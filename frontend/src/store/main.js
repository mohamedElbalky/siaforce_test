import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./authSlice";
// import credentialReducer from "./credentialSlice";

export default configureStore({
  reducer: {
    auth: authReducer,
  },
});