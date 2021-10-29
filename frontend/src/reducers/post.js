import { GET_POST } from "../actions/types.js";

const initialState = {
  post: {
    author: {},
    commentsSrc: {},
  },
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_POST:
      return {
        ...state,
        post: action.payload,
      };
    default:
      return state;
  }
}
