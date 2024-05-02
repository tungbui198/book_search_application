import ast
import pandas as pd
from utils import get_individual_from_title, remove_special_chars_keep_punct_space

# create a dictionary save language author and publisher
has_language = {}
has_author = {}
has_publisher = {}

data = pd.read_csv("./book_data_enrich.csv")

for i in range(len(data)):
    list_author = ast.literal_eval(data["hasAuthor"][i])
    for author in list_author:
        author = author
        has_author[get_individual_from_title(author)] = False
    has_publisher[get_individual_from_title(data["hasPublisher"][i])] = False
    has_language[get_individual_from_title(data["hasLanguage"][i])] = False

# this will save syntax info of author, language, publisher owl
_need_to_append = ""
# this will save syntax info of book owl
_book_to_append = ""

for i in range(len(data)):
    # for author
    list_author = ast.literal_eval(data["hasAuthor"][i])
    for name_author_individual in list_author:
        name_author_individual = remove_special_chars_keep_punct_space(
            name_author_individual
        )
        author_individual = get_individual_from_title(name_author_individual)
        if not has_author[author_individual]:
            author_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
    <ClassAssertion>
        <Class IRI="#Author"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
    <DataPropertyAssertion>
        <DataProperty IRI="#authorHasName"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
            """ % (
                author_individual,
                author_individual,
                author_individual,
                name_author_individual,
            )
            has_author[author_individual] = True
            _need_to_append += author_str

    # for publisher
    name_publisher_individual = remove_special_chars_keep_punct_space(
        data["hasPublisher"][i]
    )
    publisher_individual = get_individual_from_title(name_publisher_individual)
    if not has_publisher[publisher_individual]:
        publisher_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
    <ClassAssertion>
        <Class IRI="#Publisher"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
    <DataPropertyAssertion>
        <DataProperty IRI="#publisherHasName"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
        """ % (
            publisher_individual,
            publisher_individual,
            publisher_individual,
            name_publisher_individual,
        )
        has_publisher[publisher_individual] = True
        _need_to_append += publisher_str

    # for language
    name_language_individual = remove_special_chars_keep_punct_space(
        data["hasLanguage"][i]
    )
    language_individual = get_individual_from_title(name_language_individual)
    if not has_language[language_individual]:
        language_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
    <ClassAssertion>
        <Class IRI="#Language"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
    <DataPropertyAssertion>
        <DataProperty IRI="#languageHasName"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
        """ % (
            language_individual,
            language_individual,
            language_individual,
            name_language_individual,
        )
        has_language[language_individual] = True
        _need_to_append += language_str

    # for book
    bookTitle = remove_special_chars_keep_punct_space(data["hasTitle"][i])
    bookIndividual = get_individual_from_title(data["hasTitle"][i])
    bookId = data["hasID"][i]
    bookNumberPage = data["hasNumberPage"][i]
    bookPublicYear = data["hasPublicYear"][i]
    bookExtension = data["hasExtension"][i]
    bookSize = data["hasSize"][i]
    bookPublisher = get_individual_from_title(data["hasPublisher"][i])
    bookLanguage = get_individual_from_title(data["hasLanguage"][i])
    bookRate = data["hasRate"][i]
    bookTags = remove_special_chars_keep_punct_space(data["hasTags"][i])
    bookCategory = data["hasCategory"][i].split(",")
    bookDescription = remove_special_chars_keep_punct_space(data["hasDescription"][i])

    # create individual
    book_str = """
    <Declaration>
        <NamedIndividual IRI="#%s"/>
    </Declaration>
            """ % (
        bookIndividual
    )
    # add category
    for category in bookCategory:
        category = category.strip()
        book_str_1 = """
    <ClassAssertion>
        <Class IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ClassAssertion>
            """ % (
            category,
            bookIndividual,
        )
        book_str += book_str_1

    # add book info
    book_str_2 = """
    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#hasLanguage"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>

    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#hasPublisher"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>

    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#isPublisherOf"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasExtension"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&rdf;PlainLiteral">%s</Literal>
    </DataPropertyAssertion>
    
    <DataPropertyAssertion>
        <DataProperty IRI="#hasID"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasNumberPage"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;int">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasPublishYear"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;int">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasSize"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
    
    <DataPropertyAssertion>
        <DataProperty IRI="#hasTitle"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasTags"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>

    <DataPropertyAssertion>
        <DataProperty IRI="#hasDescription"/>
        <NamedIndividual IRI="#%s"/>
        <Literal datatypeIRI="&xsd;string">%s</Literal>
    </DataPropertyAssertion>
        """ % (
        bookIndividual,
        bookLanguage,
        bookIndividual,
        bookPublisher,
        bookPublisher,
        bookIndividual,
        bookIndividual,
        bookExtension,
        bookIndividual,
        bookId,
        bookIndividual,
        bookNumberPage,
        bookIndividual,
        bookPublicYear,
        bookIndividual,
        bookSize,
        bookIndividual,
        bookTitle,
        bookIndividual,
        bookTags,
        bookIndividual,
        bookDescription,
    )

    list_author = ast.literal_eval(data["hasAuthor"][i])
    for bookAuthorIndivdual in list_author:
        bookAuthor = get_individual_from_title(bookAuthorIndivdual)
        book_str_2 += """
    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#hasAuthor"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>
    <ObjectPropertyAssertion>
        <ObjectProperty IRI="#isAuthorOf"/>
        <NamedIndividual IRI="#%s"/>
        <NamedIndividual IRI="#%s"/>
    </ObjectPropertyAssertion>
        """ % (
            bookIndividual,
            bookAuthor,
            bookAuthor,
            bookIndividual,
        )
    book_str += book_str_2
    _book_to_append += book_str

data_to_append = _need_to_append + _book_to_append
f = open("./ontology_wo_data.owl", "r", encoding="utf8").read()
new_f = f.split("</Ontology>")
data_update = new_f[0] + "\n" + data_to_append + "</Ontology>" + new_f[1]

save_path_1 = "ontology_with_enrich_data.owl"
with open(save_path_1, "w", encoding="utf8") as owl_file:
    owl_file.write(data_update)
