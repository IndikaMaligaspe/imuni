
class Admin():
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_client_id(website, request):
        client_id = request.session.get('client_id')
        if  (client_id is not None):
            print(f" xxxx {client_id}")
        else:
            client_id = 0            
            request.session['client_id'] = client_id
            request.session.modified = True
        return client_id
    
    
