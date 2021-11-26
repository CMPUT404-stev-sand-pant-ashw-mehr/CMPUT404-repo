import { combineReducers } from "redux";
import posts from "./posts";
import post from "./post";
import followers from "./followers";
import alerts from "./alerts";
import auth from "./auth";

export default combineReducers({
  posts,
  post,
  alerts,
  followers,
  auth,
});
