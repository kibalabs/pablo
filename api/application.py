import logging
import os

from core import logging
from core.api.health import create_api as create_health_api
from core.api.middleware.database_connection_middleware import DatabaseConnectionMiddleware
from core.api.middleware.exception_handling_middleware import ExceptionHandlingMiddleware
from core.api.middleware.logging_middleware import LoggingMiddleware
from core.api.middleware.server_headers_middleware import ServerHeadersMiddleware
from core.http.basic_authentication import BasicAuthentication
from core.queues.sqs import SqsMessageQueue
from core.requester import Requester
from core.s3_manager import S3Manager
from core.store.database import Database
from core.util.value_holder import RequestIdHolder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pablo.api.api_v1 import create_api as create_v1_api
from pablo.api.static import create_api as create_static_api
from pablo.internal.ipfs_requester import IpfsRequester
from pablo.internal.model import SERVING_URL
from pablo.internal.pablo_manager import PabloManager
from pablo.store.retriever import Retriever
from pablo.store.saver import Saver

requestIdHolder = RequestIdHolder()
name = os.environ.get('NAME', 'pablo-api')
version = os.environ.get('VERSION', 'local')
environment = os.environ.get('ENV', 'dev')
isRunningDebugMode = environment == 'dev'
servingUrl = os.environ.get('SERVING_URL', SERVING_URL)

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
    IpfsRequester(ipfsPrefix='https://w3s.link/ipfs/'),
    IpfsRequester(ipfsPrefix='https://notd.infura-ipfs.io/ipfs/', headers={'Authorization': f'Basic {infuraIpfsAuth.to_string()}'}),
]
manager = PabloManager(retriever=retriever, saver=saver, requester=requester, ipfsRequesters=ipfsRequesters, workQueue=workQueue, s3Manager=s3Manager, bucketName=os.environ['BUCKET_NAME'], servingUrl=servingUrl)

app = FastAPI()
app.include_router(router=create_health_api(name=name, version=version, environment=environment))
app.include_router(prefix='/v1', router=create_v1_api(manager=manager))
app.include_router(prefix='/static', router=create_static_api(manager=manager))
app.add_middleware(ExceptionHandlingMiddleware)
app.add_middleware(ServerHeadersMiddleware, name=name, version=version, environment=environment)
app.add_middleware(LoggingMiddleware, requestIdHolder=requestIdHolder)
app.add_middleware(DatabaseConnectionMiddleware, database=database)
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_methods=['*'], allow_headers=['*'], expose_headers=['*'], allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "https://pfpkit.xyz",
    "https://milliondollartokenpage.com",
    "https://tokenhunt.io",
    "https://stormdrop.spriteclubnft.com",
    "https://gallery.milliondollartokenpage.com",
    "https://gallery.rudeboys.io",
], allow_origin_regex='https://.*\.tokenpage\.xyz')

@app.on_event('startup')
async def startup():
    await database.connect()
    await s3Manager.connect()
    await workQueue.connect()

@app.on_event('shutdown')
async def shutdown():
    for ipfsRequester in ipfsRequesters:
        await ipfsRequester.close_connections()
    await requester.close_connections()
    await s3Manager.disconnect()
    await workQueue.disconnect()
    await database.disconnect()
