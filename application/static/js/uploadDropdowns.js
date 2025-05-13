const uploadForm = document.querySelector(".upload-form");
const addPlatformButton = document.querySelector(".add-platform-button");
const removePlatformButton = document.querySelector(".remove-platform-button");
const addCategoryButton = document.querySelector(".add-category-button");
const removeCategoryButton = document.querySelector(".remove-category-button");

let platformCount = 1;
let categoryCount = 1;

function createPlatformDropdown() {
  const container = document.createElement("div");
  container.classList.add("platform-container");

  const label = document.createElement("label");
  label.textContent = "Platform: ";
  label.setAttribute("for", `platform-${platformCount}`);

  const select = document.createElement("select");
  select.name = `platform-${platformCount}`;
  select.id = `platform-${platformCount}`;
  select.classList.add("platform-dropdown");
  select.required = true;
  select.innerHTML = `
    <option value="">Select Platform</option>
    <option value="Web App">Web App</option>
    <option value="Mobile App">Mobile App</option>
    <option value="Browser Extension">Browser Extension</option>
    <option value="API">API</option>
  `;

  container.appendChild(label);
  container.appendChild(select);
  return container;
}

function createCategoryDropdown() {
  const container = document.createElement("div");
  container.classList.add("category-container");

  const label = document.createElement("label");
  label.textContent = "Category: ";
  label.setAttribute("for", `category-${categoryCount}`);

  const select = document.createElement("select");
  select.name = `category-${categoryCount}`;
  select.id = `category-${categoryCount}`;
  select.classList.add("category-dropdown");
  select.required = true;
  select.innerHTML = `
    <option value="">Select Category</option>
    <option value="Writing & Editing">Writing & Editing</option>
    <option value="Image Generation">Image Generation</option>
    <option value="Productivity & Workflow">Productivity & Workflow</option>
    <option value="Code Assistance">Code Assistance</option>
    <option value="Video & Audio Editing">Video & Audio Editing</option>
    <option value="Academic Assistance">Academic Assistance</option>
    <option value="Productivity">Productivity</option>
    <option value="Career Development">Career Development</option>
    <option value="Mental Health Support">Mental Health Support</option>
    <option value="Creative Applications">Creative Applications</option>
  `;

  container.appendChild(label);
  container.appendChild(select);
  return container;
}

addPlatformButton.addEventListener("click", (e) => {
  e.preventDefault();
  const newDropdown = createPlatformDropdown();
  const firstPlatform = uploadForm.querySelector(".platform-container");
  firstPlatform.after(newDropdown);
  platformCount++;
  removePlatformButton.style.display = "inline-block";

  if (platformCount >= 6) {
    addPlatformButton.style.display = "none"; 
  }
});

removePlatformButton.addEventListener("click", (e) => {
    e.preventDefault();
    const containers = uploadForm.querySelectorAll(".platform-container");
    if (containers.length > 1) {
        containers[containers.length - 1].remove();
        platformCount--;
    }
    if (platformCount < 6) {
        addPlatformButton.style.display = "inline-block";
    }
    if (platformCount <= 1) {
        removePlatformButton.style.display = "none";
    }
});

removePlatformButton.style.display = "none";

addCategoryButton.addEventListener("click", (e) => {
  e.preventDefault();
  const newDropdown = createCategoryDropdown();
  const firstCategory = uploadForm.querySelector(".category-container");
  firstCategory.after(newDropdown);
  categoryCount++;
  removeCategoryButton.style.display = "inline-block";

  if (categoryCount >= 3) {
    addCategoryButton.style.display = "none";
  }
});

removeCategoryButton.addEventListener("click", (e) => {
  e.preventDefault();
  const containers = uploadForm.querySelectorAll(".category-container");
  if (containers.length > 1) {
    containers[0].remove();
    categoryCount--;
  }

  if (categoryCount < 3) {
    addCategoryButton.style.display = "inline-block";
  }
  if (categoryCount <= 1) {
    removeCategoryButton.style.display = "none";
  }
});

removeCategoryButton.style.display = "none";
