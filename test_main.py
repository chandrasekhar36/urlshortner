from urlshort import create_app

def test_shorten(client):
    response=client.get('/')
    assert b'Shorten' in response.data
'''
def test_Y_URL(client):
    response=client.get('/your_url')
    assert b'Copy' in response.data
'''
