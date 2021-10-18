import { combineReducers } from "redux";
import posts from "./posts";
import alerts from "./alerts";

export default combineReducers({
  posts,
  alerts,
});
