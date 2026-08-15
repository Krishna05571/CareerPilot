import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api"
});

export const improveResume = async (text) => {
  const response = await API.post("/improve-resume", {
    text: text,
  });

  return response.data;
};

  
export default API;