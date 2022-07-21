import asyncio
import logging
import os
import time

from core import logging
from core.http.basic_authentication import BasicAuthentication
from core.queues.message_queue_processor import MessageQueueProcessor
from core.queues.sqs_message_queue import SqsMessageQueue
from core.requester import Requester
from core.s3_manager import S3Manager
from core.slack_client import SlackClient
from core.store.database import Database
from core.util.value_holder import RequestIdHolder

from pablo.internal.ipfs_requester import IpfsRequester
from pablo.internal.model import CLOUDFRONT_URL
from pablo.internal.pablo_manager import PabloManager
from pablo.internal.pablo_message_processor import PabloMessageProcessor
from pablo.store.retriever import Retriever
from pablo.store.saver import Saver


async def main():
    requestIdHolder = RequestIdHolder()
    name = os.environ.get('NAME', 'pablo-worker')
    version = os.environ.get('VERSION', 'local')
    environment = os.environ.get('ENV', 'dev')
    isRunningDebugMode = environment == 'dev'
    servingUrl = os.environ.get('SERVING_URL', CLOUDFRONT_URL)

    if isRunningDebugMode:
        logging.init_basic_logging()
    else:
        logging.init_json_logging(name=name, version=version, environment=environment, requestIdHolder=requestIdHolder)

    databaseConnectionString = Database.create_psql_connection_string(username=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"], port=os.environ["DB_PORT"], name=os.environ["DB_NAME"])
    database = Database(connectionString=databaseConnectionString)
    saver = Saver(database=database)
    retriever = Retriever(database=database)

    workQueue = SqsMessageQueue(region='eu-west-1', accessKeyId=os.environ['AWS_KEY'], accessKeySecret=os.environ['AWS_SECRET'], queueUrl='https://sqs.eu-west-1.amazonaws.com/097520841056/pablo-work-queue')
    s3Manager = S3Manager(region='eu-west-1', accessKeyId=os.environ['AWS_KEY'], accessKeySecret=os.environ['AWS_SECRET'])

    requester = Requester()
    infuraIpfsAuth = BasicAuthentication(username=os.environ['INFURA_IPFS_ID'], password=os.environ["INFURA_IPFS_SECRET"])
    ipfsRequesters = [
        IpfsRequester(ipfsPrefix='https://ipfs.io/ipfs/'),
        IpfsRequester(ipfsPrefix='https://notd.infura-ipfs.io/ipfs/', headers={'Authorization': f'Basic {infuraIpfsAuth.to_string()}'}),
        IpfsRequester(ipfsPrefix='https://kibalabs.mypinata.cloud/ipfs/'),
    ]
    pabloManager = PabloManager(retriever=retriever, saver=saver, requester=requester, ipfsRequesters=ipfsRequesters, workQueue=workQueue, s3Manager=s3Manager, bucketName=os.environ['BUCKET_NAME'], servingUrl=servingUrl)

    processor = PabloMessageProcessor(pabloManager=pabloManager)
    slackClient = SlackClient(webhookUrl=os.environ['SLACK_WEBHOOK_URL'], requester=requester, defaultSender='worker', defaultChannel='notd-notifications')
    workQueueProcessor = MessageQueueProcessor(queue=workQueue, messageProcessor=processor, slackClient=slackClient, requestIdHolder=requestIdHolder)

    await database.connect()
    await s3Manager.connect()
    await workQueue.connect()
    try:
        while True:
            hasProcessedWork = await workQueueProcessor.execute_batch(batchSize=1, longPollSeconds=1, shouldProcessInParallel=False)
            if hasProcessedWork:
                continue
            logging.info('No message received.. sleeping')
            time.sleep(60)
    finally:
        await database.disconnect()
        await s3Manager.disconnect()
        await workQueue.disconnect()
        await requester.close_connections()

if __name__ == '__main__':
    asyncio.run(main())
