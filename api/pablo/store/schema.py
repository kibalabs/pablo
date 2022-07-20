import sqlalchemy

metadata = sqlalchemy.MetaData()

ImagesTable = sqlalchemy.Table(
    'tbl_images',
    metadata,
    sqlalchemy.Column(key='imageId', name='id', type_=sqlalchemy.Text, primary_key=True, nullable=False),
    sqlalchemy.Column(key='createdDate', name='created_date', type_=sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(key='updatedDate', name='updated_date', type_=sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(key='format', name='format', type_=sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(key='filename', name='filename', type_=sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(key='width', name='width', type_=sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column(key='height', name='height', type_=sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column(key='area', name='area', type_=sqlalchemy.Integer, nullable=False),
)

ImageVariantsTable = sqlalchemy.Table(
    'tbl_image_variants',
    metadata,
    sqlalchemy.Column(key='imageVariantId', name='id', type_=sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False),
    sqlalchemy.Column(key='createdDate', name='created_date', type_=sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(key='updatedDate', name='updated_date', type_=sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(key='imageId', name='image_id', type_=sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(key='filename', name='filename', type_=sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(key='width', name='width', type_=sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column(key='height', name='height', type_=sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column(key='area', name='area', type_=sqlalchemy.Integer, nullable=False),
)

UrlUploadsTable = sqlalchemy.Table(
    'tbl_url_uploads',
    metadata,
    sqlalchemy.Column(key='urlUploadId', name='id', type_=sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False),
    sqlalchemy.Column(key='createdDate', name='created_date', type_=sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(key='updatedDate', name='updated_date', type_=sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(key='url', name='url', type_=sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(key='imageId', name='image_id', type_=sqlalchemy.Text, nullable=False),
)
