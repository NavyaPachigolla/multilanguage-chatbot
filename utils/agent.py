from utils.router import route_query
from utils.db_tool import get_student
from utils.tavily_tool import web_search


def process_query(query):

    route = route_query(query)

    if route == "database":

        if "sukruti" in query.lower():
            return get_student("Sukruti")

        elif "navya" in query.lower():
            return get_student("Navya")

        else:
            return "Student not found"

    elif route == "web":

        result = web_search(query)

        return result["results"][0]["content"]

    else:

        return "RAG response goes here"