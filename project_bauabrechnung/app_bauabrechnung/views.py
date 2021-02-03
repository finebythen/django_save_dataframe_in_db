from django.contrib import messages
from django.shortcuts import render, redirect
from django_pandas.io import read_frame
import pandas as pd
from django.utils.datastructures import MultiValueDictKeyError
from sqlalchemy import create_engine

from .models import Coworker


list_of_columns = [
        'first_name',
        'last_name',
        'age',
        'crm_id',
    ]

list_column_order = [
        'id',
        'first_name',
        'last_name',
        'age',
        'crm_id',
    ]


def main(request):

    try:
        if request.method == 'POST' and request.FILES['input-file']:
            try:
                # load database --> convert to dataframe
                qs_orig = Coworker.objects.all()
                df_orig = read_frame(qs_orig)
                df_orig.drop(['id'], axis=1, inplace=True)

                # load csv
                csv_file = request.FILES['input-file']

                # csv to dataframe --> filter for necessary columns
                df = pd.read_csv(csv_file, sep=";")
                df = df[df.columns[df.columns.isin(list_of_columns)]]

                # --> compare the two dataframes --> get the combined result
                df_comp = df.set_index('crm_id').combine_first(df_orig.set_index('crm_id')).reset_index()

                # # add needed column 'id' to dataframe --> rearrange columns
                list_id = range(1, (df_comp.shape[0] + 1))
                df_comp['id'] = list_id
                df_comp = df_comp[list_column_order]

                # convert columns of floats to integer
                df_comp['age'] = df_comp['age'].astype(int)

                # create settings for 'sqlalchemy'
                # engine = create_engine('postgresql+psycopg2://postgres:2NzxmFa2sePy@localhost:5432/db_bauabrechnung_new', echo=False)
                engine = create_engine('sqlite:///db.sqlite3', echo=False)
                conn = engine.connect()

                # save dataframe to database
                table_name = "app_bauabrechnung_coworker"
                df_comp.to_sql(table_name, conn, if_exists='replace')
                conn.close()

                # create flash message
                messages.success(request, 'Daten erfolgreich in DB importiert!')

                return redirect("Main")

            except FileNotFoundError:
                messages.error(request, 'Daten konnten nicht importiert werden!')
                pass
            except KeyError:
                messages.error(request, 'Daten konnten nicht importiert werden!')
                pass
            except ValueError:
                messages.error(request, 'Daten konnten nicht importiert werden!')
                pass
    except MultiValueDictKeyError:
        pass

    return render(request, 'app_bauabrechnung/main.html')


def overview(request):
    qs = Coworker.objects.all()

    context = {'qs': qs}
    return render(request, 'app_bauabrechnung/list.html', context)
