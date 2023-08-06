
#### Install

```console
$ python -m pip install dataco
```

#### Examples

```python
>>> from dataco import S3, GDrive

>>> s3 = S3('bucket_name')
>>> df = s3.read_csv('file_name.csv')
>>> df = s3.read_excel('file_name.xlsx', sheet_name='sheet_name')

>>> drive = GDrive('credential_file')
>>> files = drive.search_files_by_name('cities.csv')

>>> df = drive.read_csv('csv_file_id')
>>> df = drive.read_excel('excel_file_id', 'sheet_id')
```
