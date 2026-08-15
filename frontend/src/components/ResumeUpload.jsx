import { useState, useRef } from "react";
import API, { improveResume } from "../api/api";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // AI Resume Improver states
  const [resumeText, setResumeText] = useState("");
  const [improved, setImproved] = useState("");
  const [loadingImprove, setLoadingImprove] = useState(false);

  const reportRef = useRef();

  // Download the complete resume analysis as a PDF
  const downloadPDF = async () => {
    const element = reportRef.current;

    if (!element) {
      alert("No resume analysis available to download.");
      return;
    }

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
    });

    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");

    const imgWidth = 210;
    const pageHeight = 295;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(
      imgData,
      "PNG",
      0,
      position,
      imgWidth,
      imgHeight
    );

    heightLeft -= pageHeight;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;

      pdf.addPage();

      pdf.addImage(
        imgData,
        "PNG",
        0,
        position,
        imgWidth,
        imgHeight
      );

      heightLeft -= pageHeight;
    }

    pdf.save("resume-report.pdf");
  };

  // Upload resume to backend
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a resume first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      // Clear previous improved resume
      setImproved("");

      const res = await API.post("/upload-resume", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Resume upload response:", res.data);

      // Store parsed resume information
      setResult(res.data.parsed_data);

      // Store the actual cleaned resume text
      // This will later be sent to Gemini for improvement
      setResumeText(res.data.resume_text);

    } catch (err) {
      console.error("Upload error:", err);

      alert(
        err.response?.data?.detail ||
        "Upload failed"
      );
    } finally {
      setLoading(false);
    }
  };

  // Send the original resume text to Gemini for improvement
  const handleImprove = async () => {
    if (!resumeText) {
      alert("Resume text is not available.");
      return;
    }

    try {
      setLoadingImprove(true);

      // Send the complete extracted resume text
      // to the /improve-resume backend endpoint
      const data = await improveResume(resumeText);

      setImproved(data.improved);

    } catch (err) {
      console.error("Improve resume error:", err);

      alert(
        err.response?.data?.detail ||
        "Failed to improve resume"
      );
    } finally {
      setLoadingImprove(false);
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
        <h2 className="text-xl font-semibold mb-4">
          Upload Resume
        </h2>

        <input
          type="file"
          className="mb-4"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Upload"}
        </button>
      </div>

      {/* RESULT */}

      {result && (
        <div
          ref={reportRef}
          className="bg-white p-8 rounded-xl shadow-lg max-w-4xl mx-auto mt-6"
        >
          <div className="bg-white shadow-lg rounded-xl p-6 w-full max-w-3xl mt-6">

            {/* HEADER */}
            <h2 className="text-2xl font-bold">
              {result.name}
            </h2>

            <p className="text-gray-600 mb-4">
              {result.email}
            </p>

            {/* SCORE BAR */}
            <div className="mb-4">
              <p className="font-semibold mb-1">
                Resume Score: {result.resume_score}/100
              </p>

              <div className="w-full bg-gray-200 h-3 rounded-full">
                <div
                  className="bg-green-500 h-3 rounded-full transition-all duration-500"
                  style={{
                    width: `${result.resume_score}%`,
                  }}
                />
              </div>
            </div>

            {/* SKILLS */}
            <h3 className="font-semibold mb-2">
              Skills
            </h3>

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
                <h3 className="font-semibold mb-2">
                  Education
                </h3>

                <ul className="list-disc ml-5 mb-4">
                  {result.education?.map((edu, i) => (
                    <li key={i}>
                      {edu.degree} - {edu.institution} (
                      {edu.year}
                      )
                    </li>
                  ))}
                </ul>
              </div>

              {/* STRENGTHS */}
              <div>
                <h3 className="font-semibold mb-2">
                  Strengths
                </h3>

                <ul className="list-disc ml-5 mb-4">
                  {result.strengths?.map((s, i) => (
                    <li key={i}>
                      {s}
                    </li>
                  ))}
                </ul>
              </div>

              {/* WEAKNESSES */}
              <div>
                <h3 className="font-semibold mb-2">
                  Weaknesses
                </h3>

                <ul className="list-disc ml-5 mb-4">
                  {result.weaknesses?.map((w, i) => (
                    <li key={i}>
                      {w}
                    </li>
                  ))}
                </ul>
              </div>

              {/* EXPERIENCE */}
              <div>
                <h3 className="font-semibold mb-2">
                  Experience
                </h3>

                <ul className="list-disc ml-5 mb-4">
                  {result.experience?.map((exp, i) => (
                    <li key={i}>
                      {exp.role} - {exp.company} (
                      {exp.duration}
                      )
                    </li>
                  ))}
                </ul>
              </div>

            </div>

            {/* SUGGESTED ROLES */}
            <h3 className="font-semibold mt-6 mb-2">
              Suggested Roles
            </h3>

            {result.suggested_roles?.map((role, i) => (
              <div
                key={i}
                className="bg-gray-50 p-4 rounded-lg mb-3"
              >
                <p className="font-semibold">
                  {role.role}
                </p>

                <p className="text-sm text-gray-600">
                  {role.reason}
                </p>
              </div>
            ))}

            {/* SKILL GAP */}
            <h3 className="font-semibold mt-6 mb-2">
              Skill Gap Analysis
            </h3>

            {result.skill_gap_analysis?.map((gap, i) => (
              <div
                key={i}
                className="bg-gray-50 p-4 rounded-lg mb-4"
              >
                <p className="font-semibold mb-2">
                  {gap.target_role}
                </p>

                <div className="flex flex-wrap gap-2">
                  {gap.missing_skills?.map((skill, j) => (
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
            <h3 className="font-semibold mt-6 mb-2">
              Suggestions
            </h3>

            <ul className="list-disc ml-5 mb-4">
              {result.improvement_suggestions?.map(
                (s, i) => (
                  <li key={i}>
                    {s}
                  </li>
                )
              )}
            </ul>

            {/* AI RESUME IMPROVER */}
            <div className="mt-8 border-t pt-6">

              <h3 className="text-xl font-bold mb-3">
                AI Resume Improver
              </h3>

              <p className="text-gray-600 mb-4">
                Let AI rewrite your resume with stronger
                language, clearer descriptions, and
                ATS-friendly wording.
              </p>

              <button
                onClick={handleImprove}
                disabled={loadingImprove}
                className="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-lg font-medium transition disabled:opacity-50"
              >
                {loadingImprove
                  ? "Improving Resume..."
                  : "✨ Improve My Resume"}
              </button>

              {/* IMPROVED RESUME */}
              {improved && (
                <div className="mt-6 p-6 bg-purple-50 border border-purple-200 rounded-xl">

                  <h2 className="text-xl font-bold text-purple-700 mb-4">
                    ✨ AI Improved Resume
                  </h2>

                  <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                    {improved}
                  </div>

                </div>
              )}

            </div>

            {/* DOWNLOAD REPORT */}
            <div className="mt-8">

              <button
                onClick={downloadPDF}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
              >
                Download Report
              </button>

            </div>

          </div>
        </div>
      )}

    </div>
  );
}