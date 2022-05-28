from urllib import request
from jose import jwt
from social_core.backends.oauth import BaseOAuth2

class Auth0(BaseOAuth2):
    name = 'auth0'
    SCOPE_SEPARATOR = ''
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRACT_DATA = [ ("picture" , "picture") , ("email" , "email") ]

    def authorization_url(self):
        # return "https://" + 'examplepython.us.auth0.com' + "/authorize"
        return "https://" + self.setting("DOMAIN") + "/authorize"


    def access_token_url(self):
        # return "https://" + 'examplepython.us.auth0.com' + "/oauth/token"
        return "https://" + self.setting("DOMAIN") + "/oauth/token"

    
    def get_user_id(self , details , response):
        return details["user_id"]
    
    def get_user_details(self , response):
        try:
            id_token = response.get("id_token")
            # id_token = response.get("access_token")
            jwks = request.urlopen(
                # "https://" + 'examplepython.us.auth0.com' + "/.well-known/jwks.json"
                "https://" + self.setting("DOMAIN") + "/.well-known/jwks.json"
            )
            
            # issuer = "https://" + 'examplepython.us.auth0.com' + ""
            issuer = "https://" + self.setting("DOMAIN") + "/"

            # audience = self.settings("KEY")
            audience = 'v1nqI3DvxbYsBSSHFEn6HUApAGlL6TRv'

            payload = jwt.decode(
                id_token,
                jwks.read(),
                algorithms= ['RS256'],
                audience = audience,
                issuer = issuer,
            )

            return {
                "username": payload["nickname"],
                "first_name": payload["name"],
                "pictures" : payload["picture"],
                "user_id": payload["sub"],
                "email": payload["email"],
            }
        except Exception as e:
            print(str(e))