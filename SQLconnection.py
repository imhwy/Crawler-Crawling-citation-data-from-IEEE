# import libraries
import pypyodbc
import xml.etree.ElementTree as ET


# implement the connection to SQL SERVER
class mysql_server:
    def __init__(self, server, database):
        self.server = server
        self.database = database

    def connect_server(self):
        conn = pypyodbc.connect(
            "Driver={SQL SERVER};"
            f"Server={self.server};"
            f"Database={self.database};"
            "Trusted_Connection=yes;"
        )
        return conn

    def create_author_table(self, cursor):
        cursor.execute(
            """
        CREATE TABLE AuthorInformations
        (ID INT PRIMARY KEY, Author VARCHAR(255), TiTle VARCHAR(355))
        """
        )
        return cursor

    def insert_author_table(self, cursor, name, articles, conn, iD):
        iD += 1
        for ar in articles:
            try:
                title = ar.find(".//title").text
            except:
                title = ar.find(".//i").text
            cursor.execute(
                "INSERT INTO AuthorInformations (ID, Author, Title) VALUES (?, ?, ?)",
                (
                    iD,
                    name,
                    title,
                ),
            )
            conn.commit()
            iD += 1
        return conn

    def create_table(self, cursor, file_name):
        name = file_name.replace(".xml", "")
        cursor.execute(
            """
            CREATE TABLE {}
            (ID INT PRIMARY KEY, IDPaper INT, AuthorAndCoauthor VARCHAR(955), Title VARCHAR(355), Pages VARCHAR(255), Year INT, Volume VARCHAR(255), Booktitle VARCHAR(255), Journal VARCHAR(255), ee VARCHAR(255), crossref VARCHAR(255), url_link VARCHAR(255))
            """.format(
                name
            )
        )
        return cursor

    def parse_xml(self, file_xml):
        tree = ET.parse(file_xml)
        articles = tree.findall("r")
        return articles

    def insert_information(self, articles, cursor, conn, file_name, iD_paper):
        iD = 1
        iD_paper += 1
        name = file_name.replace(".xml", "")
        for ar in articles:
            try:
                authors = [author.text for author in ar.findall(".//author")]
                author = ", ".join(authors)
            except:
                author = None
            title = ar.find(".//title").text
            if title == None:
                title = f"Not finding {iD}"
            try:
                page = ar.find(".//pages").text
            except:
                page = None
            try:
                year = ar.find(".//year").text
            except:
                year = None
            try:
                volume = ar.find(".//volume").text
            except:
                volume = None
            try:
                booktitle = ar.find(".//booktitle").text
            except:
                booktitle = None
            try:
                journal = ar.find(".//journal").text
            except:
                journal = None
            try:
                ee = ar.find(".//ee").text
            except:
                ee = None
            try:
                crossref = ar.find(".//crossref").text
            except:
                crossref = None
            try:
                url_link = ar.find(".//url").text
            except:
                url_link = None
            try:
                cursor.execute(
                    "INSERT INTO {} (ID, IDPaper , AuthorAndCoauthor, Title, Pages, Year, Volume, Booktitle, Journal, ee, crossref, url_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
                        name
                    ),
                    (
                        iD,
                        iD_paper,
                        author,
                        title,
                        page,
                        year,
                        volume,
                        booktitle,
                        journal,
                        ee,
                        crossref,
                        url_link,
                    ),
                )
                conn.commit()
            except:
                continue
            iD_paper += 1
            iD += 1
