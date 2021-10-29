import axios from "axios";

import { GET_INBOX } from "./types";

import { tokenConfig } from "./auth";

export const getInbox =
  (pageUrl = "") =>
  (dispatch, getState) => {
    let page = 1;
    if (pageUrl) {
      const url = new URL(pageUrl);
      const urlparams = new URLSearchParams(url.search);
      page = urlparams.has("page") ? urlparams.get("page") : 1;
    }

    const authorId = getState().auth.user.author;

    axios
      .get(`/author/${authorId}/inbox`, tokenConfig(getState))
      .then((res) => {
        dispatch({
          type: GET_INBOX,
          payload: res.data,
          page: page,
        });
      })
      .catch((err) => {
        const alert = {
          msg: err.response.data,
          status: err.response.status,
        };
        dispatch({
          type: GET_ALERTS,
          payload: alert,
        });
      });
  };
