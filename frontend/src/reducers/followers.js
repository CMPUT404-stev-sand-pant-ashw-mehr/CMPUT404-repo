import {
  GET_FOLLOWERS,
  DELETE_FOLLOWER,
  ADD_FOLLOWER,
  CHECK_FOLLOWER,
} from "../actions/types.js";

const initialState = {
  followers: [],
};

export default function (state = initialState, action) {
  switch (action.type) {
    case DELETE_FOLLOWER:
    case ADD_FOLLOWER:
    case CHECK_FOLLOWER:
      return {
        ...state,
        followers: action.payload,
      };
    case GET_FOLLOWERS:
      return {
        ...state,
        followers: action.payload,
      };
    default:
      return state;
  }
}
