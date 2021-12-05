import axios from "axios";
import {
  CREATE_ALERT,
  USER_LOADING,
  USER_LOADED,
  AUTH_ERROR,
  LOGIN_SUCCESS,
  LOGOUT_SUCCESS,
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  GET_AUTHORS,
} from "./types";

export const tokenConfig = (getState) => {
  const token = getState().auth.token;

  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (token) {
    config.headers["Authorization"] = `Token ${token}`;
  }

  return config;
};
export const loadUser = () => (dispatch, getState) => {
  dispatch({
    type: USER_LOADING,
  });

  axios
    .get("/auth/profile", tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: USER_LOADED,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { error: "Authentication error!" },
          status: err.response.status,
        },
      });
      localStorage.removeItem("token");
      dispatch({
        type: AUTH_ERROR,
      });
    });
};

export const login = (username, password) => (dispatch) => {
  const body = JSON.stringify({ username, password });
  axios
    .post("/auth/login", body, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((res) => {
      localStorage.setItem("token", res.data.token);
      dispatch({
        type: LOGIN_SUCCESS,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { error: "Invalid credentials entered!" },
          status: err.response.status,
        },
      });
      dispatch({
        type: AUTH_ERROR,
      });
    });
};

export const register =
  ({ username, displayName, github, email, password }) =>
  (dispatch) => {
    const body = JSON.stringify({
      username,
      displayName,
      github,
      email,
      password,
    });
    axios
      .post("/auth/register", body, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((res) => {
        localStorage.setItem("token", res.data.token);
        dispatch({
          type: REGISTER_SUCCESS,
          payload: res.data,
        });
        dispatch({
          type: CREATE_ALERT,
          payload: {
            msg: {
              success:
                "Success! Please wait to login until you are superadmin approved.",
            },
            status: res.status,
          },
        });
        window.location.href = "#/login";
      })
      .catch((err) => {
        dispatch({
          type: CREATE_ALERT,
          payload: {
            msg: err.response.data,
            status: err.response.status,
          },
        });
        dispatch({
          type: REGISTER_FAIL,
        });
      });
  };

export const logout = () => (dispatch, getState) => {
  axios
    .post("/auth/logout/", null, tokenConfig(getState))
    .then(() => {
      dispatch({
        type: LOGOUT_SUCCESS,
      });
    })
    .catch((err) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { error: err.response.data },
          status: err.response.status,
        },
      });
      localStorage.removeItem("token");
    });
};

export const getAuthors = () => (dispatch, getState) => {
  axios
    .get(`/authors/`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_AUTHORS,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { error: "Failed to get authors!" },
          status: err.response.status,
        },
      });
    });
};
