import { CREATE_ALERT } from "./types";

export const createError = (msg) => (dispatch) => {
  dispatch({
    type: CREATE_ALERT,
    payload: {
      msg: { error: msg },
      status: "error",
    },
  });
};
