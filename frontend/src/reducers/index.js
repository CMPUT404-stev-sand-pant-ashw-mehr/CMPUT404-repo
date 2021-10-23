import { combineReducers } from "redux";
import posts from "./posts";
import alerts from "./alerts";
import auth from "./auth";

export default combineReducers({
  posts,
  alerts,
  auth,
});
