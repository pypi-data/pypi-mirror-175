
#### To install

`python -m pip dataco`


#### Examples

```python
>>> from dataco import S3, GDrive

>>> s3 = S3('bucket_name')
>>> df = s3.read_csv('file_name.csv')

>>> drive = GDrive('credential_file')
>>> df = drive.read_excel('file_name.xlsx', 'sheet_id')

>>> files = drive.search_files_by_name('cities.csv')
```
