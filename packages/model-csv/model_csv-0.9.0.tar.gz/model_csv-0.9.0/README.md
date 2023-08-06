# django-csv
django-csv makes it easy to treat csv, tsv and excel file.

# How to use django-csv.
## Create ModelCsv
```python3
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookCsv(ModelCsv):
    class Meta:
        model = Book
        # if you defined fields then ModelCsv create columns automatically.
        fields = '__all__'
```

## Use as write mode
```python3
# Create 2d list of model values from queryset
mcsv = BookCsv.for_write(instances=Book.objects.all())
mcsv.get_table(header=True)
[['title', 'price', 'is_on_sale', 'description'], ['Book title', '540', 'YES', 'description']]
```
## Use as read mode
```python3
# Create django model from csv file.
with open('book.csv', 'r') as f:
    reader = CsvReader(file=f,table_starts_from=1)
    table = reader.get_table()
mcsv = BookCsv.for_read(table=table)

# get value as dict
mcsv.get_as_dict()  # list of dict
[{'title': 'Book title', 'price': 540, 'is_on_sale': True, 'description': 'description'}, ...]

# get instances (unsaved)
instances = list(mcsv.get_instance())

# bulk create django model
mcsv.bulk_create(batch_size=100)
```

## Easy to use in Class-Based Views.
```python3
# Download csv file in django view.
class BookDownloadView(generic.View):
    def get(self, **kwargs):
        book_csv = BookCsv.for_write(instance=Book.objects.all())
        writer = CsvWriter(file_name='book.csv')
        return book_csv.get_response(writer=writer)

# Upload csv file in django view.
class BookUploadView(generic.View):
    def post(self, **kwargs):
        # e.g. [['Book title', '540', 'YES', 'description'],]
        table = CsvReader(file=file_object, table_starts_from=1).get_table()
        book_csv = BookCsv.for_read(table=table)
        # create book model.
        book_csv.bulk_create()
        return redirect(self.get_success_url)
```

## django-csv is a Class-Based Csv Manager.
ModelCsv can define header, column order and type of value by Column class.
And You can define, validate and fix values in ModelCsv methods.
Therefore, you don't have to write spaghetti code in django view anymore.

## Annoying spaghetti code example.
```python

class BookDownloadCsv(generic.View):
    def post(self, **kwargs):
        header = [
            'Book Title',
            'Now On sale',
            'R18',
            'Price',
            'Publish Date',
            'Memo',
            'Description',
            'Csv Output Date',
            # Suppose columns over 20 ...
        ]
        body = [header]
        today = timezone.now().date()
        for book in Book.objects.all():
            title = book.title.replace(N_WORD, '*', len(N_WORD))
            if book.is_restricted_under_18:
                title = '[R18]' + title
            
            price = f'${book.price or 0}'
            if book.published_at:
                published_at = book.published_at.strftime('%Y-%m-%d')
            else:
                published_at = 'TBD'
                title = '(TBD)' + title  # values are sometimes fixed at several points.
                price += ' (Unsettled)'
            
            # Suppose each values need to be fixed depends on other values ... 
            body += [
                title,
                'YES' if book.is_on_sale else 'NO',
                'YES' if book.is_restricted_under_18 else 'NO',
                price,
                published_at,
                '',
                '',
                today,
                # You have to check if order of values is valid ... 
            ]
        return # create csv file and return response.
```

Cool Solution with django-csv
```python
class BookCsv(ModelCsv):
    # MethodColumn is a column which returns a result of `column_*` method.
    title = columns.MethodColumn(header='Book Title')

    # AttributeColumn is a column which returns an attribute of model. 
    is_on_sale = columns.AttributeColumn(header='Now On Sale', to=bool)
    is_restricted_under_18 = columns.AttributeColumn(header='R18', to=bool)
    price = columns.MethodColumn(header='Price')
    published_at = columns.AttributeColumn(header='Publish Date')

    # StaticColumn is a column which always returns `static_value.`
    memo = columns.StaticColumn(header='Memo', static_value='')
    description = columns.StaticColumn(header='Description')
    csv_output_date = columns.StaticColumn(header='Csv Output Date')
    # even if columns over 20, it's not so difficult to manage order.

    class Meta:
        model = Book
        read_mode = False  # if False, then this class cannot call Csv.for_read()
        # if auto_assign is true, column indexed are automatically assigned.
        # Assigned indexes are equal to the declaration order of columns.
        auto_assign = True

    def column_title(self, instance: Book, **kwargs) -> str:
        # Special methods with `column_` prefix are called when write down to a csv file.
        title = instance.title.replace(N_WORD, '*' * len(N_WORD))
        if instance.is_restricted_under_18:
            title = '[R18] ' + title
        if instance.is_restricted_under_18:
            title = '(TBD)' + title
        return title

    def column_published_at(self, instance: Book, **kwargs) -> Union[datetime, stre]:
        pbl_at = instance.published_at
        return pbl_at.strftime('%Y-%m-%d') if pbl_at else 'TBD'

    def column_price(self, instance: Book, **kwargs) -> str:
        price = f'${instance.price or 0}'
        if not instance.published_at:
             price += ' (Unsettled)'

        return price


class BookDownloadView(generic.View):
    # you can keep your view simpler.
    def post(self, **kwargs):
        # call as write mode.
        book_csv = BookCsv.for_write(instances=Book.objects.all())
        # you can insert value after construct ModelCsv.
        book_csv.set_static_column('csv_output_date', timezone.now().date())
        # define filename and file type. Other choices are TsvWriter, ExcelWriter ...
        writer = CsvWriter(file_name='book.csv')
        return book_csv.get_response(writer=writer)
```


## ForeignKey?