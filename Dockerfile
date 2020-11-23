# Derived from: https://romandc.com/zappa-django-guide/setup/#approach-2-docker-with-zappa-recommended
FROM lambci/lambda:build-python3.8

# Download and install SQLite from source to generate _sqlite3.so
# Source: https://charlesleifer.com/blog/compiling-sqlite-for-use-with-python-applications/
# Note: sqlite-33001 refers to SQLite 3.30.1
RUN yum install -y tcl
WORKDIR /usr/
RUN curl https://www.sqlite.org/src/tarball/sqlite-33001.tar.gz | tar xz
WORKDIR /usr/sqlite-33001/
RUN ./configure && make sqlite3.c
WORKDIR /usr/
RUN git clone https://github.com/coleifer/pysqlite3
WORKDIR /usr/pysqlite3/
RUN cp /usr/sqlite-33001/sqlite3.[ch] .
RUN python setup.py build_static && python setup.py install

WORKDIR /var/task

RUN cp /var/lang/lib/python3.8/site-packages/pysqlite3-0.4.4-py3.8-linux-x86_64.egg/pysqlite3/_sqlite3.cpython-38-x86_64-linux-gnu.so .

COPY . .

RUN poetry install --no-dev

CMD ["poetry", "run", "zappa", "update"]
