// src/firebaseAuth.js
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCSIqys1rMyeLiHxce-cRanLT9vl42lwig",
  authDomain: "ad-camp-62ef4.firebaseapp.com",
  projectId: "ad-camp-62ef4",
  storageBucket: "ad-camp-62ef4.appspot.com",
  messagingSenderId: "222309474137",
  appId: "1:222309474137:web:8ca7a36c1110b7829b7648",
  measurementId: "G-Y33HQ7DPVQ"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
provider.addScope('openid');
provider.addScope('https://www.googleapis.com/auth/userinfo.email');
provider.addScope('https://www.googleapis.com/auth/userinfo.profile');


export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    const credential = GoogleAuthProvider.credentialFromResult(result);
    const token = credential.idToken;
    return token;
  } catch (error) {
    console.error("Error signing in with Google", error);
    throw error;
  }
};