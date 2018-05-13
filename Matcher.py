import gensim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import linear_kernel
import csv
from textblob import TextBlob as tb
import Utils


#with the cosine similarity we want to put the document we are comparing to through the tf-idf algorithm to find the importance of the words
#then we need to match up the keywords using the cosine similarity of the documents
#step 1 read in the CV
#step 2 find the keywords using the tf-idf implementation and the documents we already have
#step 3 apply the cosine similarity to all the documents and this one and see if they match up


def gensim_document_similarity():
    pass

def scikitlearn_document_similarity():
    corpus = Utils.get_corpus_from_descriptions()
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus).todense()

    euclideanDistances = []
    index = 0
    for f in features:
        euclideanDistances.append({"distance": euclidean_distances(features[1], f)[0], "description": corpus[index]})
        index = index + 1

    for e in sorted(euclideanDistances[:10], key=lambda x: x["distance"]):
        print(e)

def custom_cosine_similarity():
    pass

def scikitlearn_document_similarity_using_TfidfVectorizer(text_to_compare):
    corpus_dict = Utils.get_corpus_from_descriptions(text_to_compare)
    corpus = [d['description'] for d in corpus_dict]
    tfidf = TfidfVectorizer().fit_transform(corpus)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    for i in related_docs_indices:
        print(corpus_dict[i-1]['title'])
        print(corpus_dict[i-1]['description'])
    print(cosine_similarities[related_docs_indices])

scikitlearn_document_similarity_using_TfidfVectorizer("Sample Resumes CVhttp://sample-resumes-cv.blogspot.com•Written stored procedures, triggers using SQL in SQL SERVER 2000.Developed Cascading Style Sheets (CSS) for User Interface uniformity throughout theapplication.•Developed and consumed Web Services for Speech Analysis and Integration with KeefeCommissary.•Used HTML, JavaScript and AJAX for developing Controls and web forms in Debit AccountingSoftware.•Extensively used GridViews with sorting and paging•Implemented Template Columns for Custom Nested GridViews.•Developed XSL, XSD files for Media Metadata XML files.•Developed User Documents for the users.•Provided Production support.Environment:ASP.NET2.0, ADO.NET, Microsoft Visual Stuidio.NET 2005, IIS V5.1, SQL , HTML,SQL Server 2000 Query Analyzer, SQL Profiler,.NET Framework 2.0, and Windows 2003 server Client: Date - DateRole: .Net Developer Project: Rent-A-Toll -Toll Solutions for Car RentersRent-A-Toll – provides solution for car renters to violate toll lanes through out their journey and pay for it at once. This solution saves lot of time for the renters and with different products provided by thecompany, they end up saving money too. Three Web portals are under development andenhancement for this solution, they are RTL portal used by Employees of Rent A Toll, Toll Authoritiesand Rental Car Agencies. Rent-A-Toll Employees can log in and set up Toll Authorities and Rental Car Agency they are going to work with. They can send Invoices to Rental Car Agencies and Deposits tothe Toll Authorities. The Toll Authorities can log in and view deposits sent Rent-A-Toll, the Violationsmade by customers. The Rental Car Agency employees can log in and view Invoice, enter Customer Payments and Dispute the invoice. The Other portal is Customer Portal which provides Customer Service. The Customer can check the violations they made, where and when they exactly made theviolation. The third portal is Reports portal showing sales and Revenue reports.Responsibilities:•Used N-tier architecture for presentation layer, the Business and Data Access Layers and werecoded using C#.•Developed application logic using C#.•Written stored procedures, triggers using SQL in SQL SERVER 2005.•Worked intensely on the User Interface.•Developed WebForms using C# and ASP.NET.•Used AJAX in some webforms.•Worked on Cascading Style Sheets and XML-Schemas.•Developed Web Services for user authentication and file ransfer •Used Xpath , XmlNode to access files and XMLDataDocument to synchronize with Datasets.•Compared the XML files sent by the Toll Authorities with XML Schemas.•Ensured Security to all the portals by creating Tampered proofed URLs.•Wrote triggers for sending Emails after to clients after any kind of transaction has been made•Extensively used GridViews sorting and paging•Implemented Template Columns for Custom Nested GridViews•Worked with Infragistic Controls extensively.•Worked on exporting reports to Excel from Gridviews and Ultrawebgrids.•Deployment of Application on Test and Production Server.•Handled many production issues and enhancement to the existing live portalsEnvironment: ASP.NET2.0, C#.NET, ADO.NET, Microsoft Visual Stuidio.NET 2005, IIS 5.0, SQL,XML, XSL, HTML, SQL Server 2000 Enterprise Manager, SQL Server 2005 Query Analyzer, .NETFramework 2.0, and Windows 2003 server EDUCATIONDegree from Ozmania University - 1996")