document.getElementById("user_type").addEventListener("change", function(event) {
    const selectedType = event.target.value;
    if (selectedType === "Student") {
      document.getElementById("student_fields").style.display = "block";
      document.getElementById("company_fields").style.display = "none";
    } else if (selectedType === "Company") {
      document.getElementById("company_fields").style.display = "block";
      document.getElementById("student_fields").style.display = "none";
    } else {
      document.getElementById("student_fields").style.display = "none";
      document.getElementById("company_fields").style.display = "none";
    }
  });
  