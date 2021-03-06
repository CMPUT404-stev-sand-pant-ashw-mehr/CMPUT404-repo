import { GET_INBOX } from "../actions/types.js";

const initialState = {
  items: [],
  next: "",
  previous: "",
  page: 1,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_INBOX:
      return {
        ...state,
        items: action.payload.items,
        next: action.payload.next,
        previous: action.payload.previous,
        page: action.page,
      };
    default:
      return state;
  }
}
