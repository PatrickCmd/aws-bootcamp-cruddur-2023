import { Auth } from 'aws-amplify';
import { resolvePath } from 'react-router-dom';

export async function getAccessToken() {
  Auth.currentSession()
    .then((cognito_user_session) => {
      const access_token = cognito_user_session.accessToken.jwtToken
      localStorage.setItem("access_token", access_token)
    })
    .catch((err) => console.log(err));
}

export async function checkAuth(setUser) {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false
  })
    .then((cognito_user) => {
      setUser({
        cognito_user_uuid: cognito_user.attributes.sub,
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
      const current_user = {
        "sub": cognito_user.attributes.sub,
        "name": cognito_user.attributes.name,
        "preferred_username": cognito_user.attributes.preferred_username,
        "email": cognito_user.attributes.email
      }
      localStorage.setItem("current_user", JSON.stringify(current_user))
      return Auth.currentSession()  // current session with refreshed access token.
    }).then((cognito_user_session) => {
      localStorage.setItem("access_token", cognito_user_session.accessToken.jwtToken)
    })
    .catch((err) => console.log(err));
};