import { CREATE_ALERT, GET_ALERTS } from "../actions/types";

const initialState = {
  msg: {},
  status: null,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_ALERTS:
    case CREATE_ALERT:
      return {
        msg: action.payload.msg,
        status: action.payload.status,
      };
    default:
      return state;
  }
}
