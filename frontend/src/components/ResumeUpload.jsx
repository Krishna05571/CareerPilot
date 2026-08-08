import { useState } from "react";
import API from "../api/api";

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await API.post("/upload-resume", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(res.data.parsed_data);
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">

      {/* Title */}
      <h1 className="text-4xl font-bold mb-6 text-gray-800">
        AI Career Mentor 🚀
      </h1>

      {/* Upload Card */}
      <div className="bg-white shadow-lg rounded-xl p-6 w-full max-w-3xl">
        <h2 className="text-xl font-semibold mb-4">Upload Resume</h2>

        <input
          type="file"
          className="mb-4"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button
          onClick={handleUpload}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          {loading ? "Analyzing..." : "Upload"}
        </button>
      </div>

      {/* RESULT */}
      {result && (
        <div className="bg-white shadow-lg rounded-xl p-6 w-full max-w-3xl mt-6">

          {/* HEADER */}
          <h2 className="text-2xl font-bold">{result.name}</h2>
          <p className="text-gray-600 mb-4">{result.email}</p>

          {/* SCORE BAR */}
          <div className="mb-4">
            <p className="font-semibold mb-1">
              Resume Score: {result.resume_score}/100
            </p>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-green-500 h-3 rounded-full"
                style={{ width: `${result.resume_score}%` }}
              ></div>
            </div>
          </div>

          {/* SKILLS */}
          <h3 className="font-semibold mb-2">Skills</h3>
          <div className="flex flex-wrap gap-2 mb-6">
            {result.skills?.map((skill, i) => (
              <span
                key={i}
                className="bg-black text-green-400 px-3 py-1 rounded-full text-sm"
              >
                {skill}
              </span>
            ))}
          </div>

          {/* GRID SECTION */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {/* EDUCATION */}
            <div>
              <h3 className="font-semibold mb-2">Education</h3>
              <ul className="list-disc ml-5 mb-4">
                {result.education?.map((edu, i) => (
                  <li key={i}>
                    {edu.degree} - {edu.institution} ({edu.year})
                  </li>
                ))}
              </ul>
            </div>

            {/* STRENGTHS */}
            <div>
              <h3 className="font-semibold mb-2">Strengths</h3>
              <ul className="list-disc ml-5 mb-4">
                {result.strengths?.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>

            {/* WEAKNESSES */}
            <div>
              <h3 className="font-semibold mb-2">Weaknesses</h3>
              <ul className="list-disc ml-5 mb-4">
                {result.weaknesses?.map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            </div>

            {/* EXPERIENCE */}
            <div>
              <h3 className="font-semibold mb-2">Experience</h3>
              <ul className="list-disc ml-5 mb-4">
                {result.experience?.map((exp, i) => (
                  <li key={i}>
                    {exp.role} - {exp.company} ({exp.duration})
                  </li>
                ))}
              </ul>
            </div>

          </div>

          {/* SUGGESTED ROLES */}
          <h3 className="font-semibold mt-6 mb-2">Suggested Roles</h3>
          {result.suggested_roles?.map((role, i) => (
            <div key={i} className="bg-gray-50 p-4 rounded-lg mb-3">
              <p className="font-semibold">{role.role}</p>
              <p className="text-sm text-gray-600">{role.reason}</p>
            </div>
          ))}

          {/* SKILL GAP */}
          <h3 className="font-semibold mt-6 mb-2">Skill Gap Analysis</h3>
          {result.skill_gap_analysis?.map((gap, i) => (
            <div key={i} className="bg-gray-50 p-4 rounded-lg mb-4">
              <p className="font-semibold mb-2">{gap.target_role}</p>
              <div className="flex flex-wrap gap-2">
                {gap.missing_skills.map((skill, j) => (
                  <span
                    key={j}
                    className="bg-red-100 text-red-600 px-2 py-1 rounded text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}

          {/* SUGGESTIONS */}
          <h3 className="font-semibold mt-6 mb-2">Suggestions</h3>
          <ul className="list-disc ml-5 mb-4">
            {result.improvement_suggestions?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

        </div>
      )}
    </div>
  );
}