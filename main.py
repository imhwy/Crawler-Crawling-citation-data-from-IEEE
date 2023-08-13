# import module
import crawler
import SQLconnection
from crawler import crawling
from SQLconnection import mysql_server


def main():

    # insert server, database, number of authors and their names
    server = input("Enter the server name: ")
    database = input("Enter the database name: ")
    n = int(input("Enter the number of author: "))
    author_name_list = []
    for i in range(n):
        temp_author_name = input(f"Enter the author's name ({i+1}): ")
        author_name_list.append(temp_author_name)

    # create an instance of mysql_server
    SQL_connect = mysql_server(server, database)
    conn = SQL_connect.connect_server()
    cursor = conn.cursor()
    SQL_connect.create_author_table(cursor)
    table_name_list = []
    iD = 1000

    # start crawling and save into database
    for name in author_name_list:
        browser = crawler.webdriver.Chrome(executable_path="chromedriver.exe")
        crawler_dblp = crawling(browser)
        crawler_dblp.navigate_to_dblp()
        crawler_dblp.author_searching_function(name)
        xml_link = crawler_dblp.access_author_link()
        file_name = crawler_dblp.download_xml(name, xml_link)
        cursor = SQL_connect.create_table(cursor, file_name)
        articles = SQL_connect.parse_xml(file_name)
        SQL_connect.insert_information(articles, cursor, conn, file_name, iD)
        SQL_connect.insert_author_table(cursor, name, articles, conn, iD)
        table_name_list.append(file_name)
        iD += 1000

    # create relational database
    for table_name in table_name_list:
        name = table_name.replace(".xml", "")
        try:
            cursor.execute(
                "ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY (IDPaper) REFERENCES AuthorInformations (ID)".format(
                    name, "fk_" + name
                )
            )
        except Exception as e:
            print(
                "Error creating foreign key constraint for table {}: {}".format(name, e)
            )

    # close conn and cursor
    conn.close()
    cursor.close()


# run code
if __name__ == "__main__":
    main()
