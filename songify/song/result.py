from django.http import HttpResponse


class Result:
    """
    class with the static method to take the data and 
    return the Http Response
    """
    @staticmethod
    def BuildResult(data, status):
        return HttpResponse(data, status=status)
