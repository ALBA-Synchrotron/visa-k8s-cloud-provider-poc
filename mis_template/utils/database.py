# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import MySQLdb


def dict_fetch_all(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetch_one(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))


class LegacyDatabaseConnector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.connection:
            self.logger.info('Connection already created to legacy database. No need to re-connect.')
            return

        try:
            # Be careful: by default the server is localhost. It should find the file
            self.logger.info('Trying to connect: %s' % (MySQLdb.connect(read_default_file='../config/database/legacy.cnf')))
            self.connection = MySQLdb.connect(read_default_file='../config/database/legacy.cnf')
            self.logger.info('Connection created success to legacy database')
        except MySQLdb.Error as e:
            self.logger.error('Error connecting to legacy database: ' + str(e))

    def get_cursor(self):
        if not self.connection:
            self.logger.debug('Creating connection to setup a cursor')
            self.connect()

        if not self.cursor:
            self.logger.debug('Creating cursor')
            self.cursor = self.connection.cursor()

        return self.cursor

    def commit(self):
        if self.connection:
            self.connection.commit()
            self.logger.info('Transaction commit success')
            return

        self.logger.warning('Commit could not be done due to no connection available')

    def rollback(self):
        if self.connection:
            self.connection.rollback()
            self.logger.info('Transaction rollback success')
            return

        self.logger.warning('Rollback could not be done due to no connection available')

    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info('Connection close success')
            return

        self.logger.warning('Close could not be done due to no connection available')
