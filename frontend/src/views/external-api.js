import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";

const ExternalApi = () => {
  const [response, setResponse] = useState("");
  const [token, setToken] = useState("");
  const serverUrl = process.env.REACT_APP_SERVER_URL;

  const { getAccessTokenSilently } = useAuth0();

  const refreshToken = async () => {
    try {
      const accessToken = await getAccessTokenSilently();
      setToken(accessToken);
    } catch (error) {
      console.log(error.message);
    }
  };

  useEffect(() => {
    refreshToken();
  });

  const callSecureApi = async () => {
    // await getToken();
    try {
      const response = await fetch(`${serverUrl}/actors`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const responseData = await response.json();
      console.log(responseData);

      // setResponse(responseData);
    } catch (error) {
      setResponse(error.message);
    }
  };

  return (
    <div className="container">
      <h1>External API</h1>
      <p>
        Use these buttons to call an external API. The protected API call has an
        access token in its authorization header. The API server will validate
        the access token using the Auth0 Audience value.
      </p>
      <div
        className="btn-group mt-5"
        role="group"
        aria-label="External API Requests Examples"
      >
        <button
          type="button"
          className="btn btn-primary"
          onClick={refreshToken}
        >
          Get Token
        </button>
        <button
          type="button"
          className="btn btn-primary"
          onClick={callSecureApi}
        >
          Get Protected Message
        </button>
      </div>
      {token && (
        <div className="mt-5">
          <h6 className="muted">Token</h6>
          <div className="container-fluid">
            <div className="row">
              <code className="col-12 text-light bg-dark p-4">{token}</code>
            </div>
          </div>
        </div>
      )}
      {response && (
        <div className="mt-5">
          <h6 className="muted">response</h6>
          <div className="container-fluid">
            <div className="row">
              <code className="col-12 text-light bg-dark p-4">{response}</code>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExternalApi;
