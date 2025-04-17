const searchForm = document.querySelector(".search-form");
const addFilterButton = document.querySelector(".add-filter-button");
const removeFilterButton = document.querySelector(".remove-filter-button");
const optionsData = {
  categories: ["Writing & Editing", "Image Generation", "Productivity & Workflow", "Code Assistance", "Video & Audio Editing",
               "Academic Assistance", "Productivity", "Career Development", "Mental Health Support", "Creative Applications"],
  platform: ["Web App", "Mobile App", "Browser Extension", "Desktop", "Software", "API"],
  publishing: ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
};
let filterCount = 1;

function createFilterDropdowns() {
  const newFilterContainer = document.createElement("div");
  newFilterContainer.classList.add("filter-container");

  const filterSelect = document.createElement("select");
  filterSelect.name = "filters[]";
  filterSelect.classList.add("filter-dropdown");
  filterSelect.innerHTML = `
        <option class="dropdown-option" value="">Filter</option>
        <option class="dropdown-option" value="categories">Categories</option>
        <option class="dropdown-option" value="platform">Platform</option>
        <option class="dropdown-option" value="publishing">Publishing Date</option>
    `;

  const optionsSelect = document.createElement("select");
  optionsSelect.name = "filter-options[]";
  optionsSelect.classList.add("filter-dropdown");
  optionsSelect.innerHTML =
    '<option class="dropdown-option" value="">Option</option>';

  filterSelect.addEventListener("change", function () {
    updateOptions(this, optionsSelect);
  });

  newFilterContainer.appendChild(filterSelect);
  newFilterContainer.appendChild(optionsSelect);
  return newFilterContainer;
}

function updateOptions(filterDropdown, optionsDropdown) {
  const selectedFilter = filterDropdown.value;
  optionsDropdown.innerHTML =
    '<option class="dropdown-option" value="">Option</option>';

  if (optionsData[selectedFilter]) {
    optionsData[selectedFilter].forEach((option) => {
      const optionElement = document.createElement("option");
      optionElement.classList.add("dropdown-option");
      optionElement.textContent = option;
      optionsDropdown.appendChild(optionElement);
    });
  }
}

const initialFilterContainer = searchForm.querySelector(".filter-container");
const initialFilterSelect = initialFilterContainer.querySelector(
  'select[name="filters[]"]'
);
const initialOptionsSelect = initialFilterContainer.querySelector(
  'select[name="filter-options[]"]'
);
if (initialFilterSelect) {
  initialFilterSelect.addEventListener("change", function () {
    updateOptions(this, initialOptionsSelect);
  });
}

addFilterButton.addEventListener("click", function (event) {
  event.preventDefault();

  if (filterCount < 3) {
    const newDropdowns = createFilterDropdowns();
    searchForm.insertBefore(
      newDropdowns,
      searchForm.querySelector(".search-bar")
    );
    filterCount++;
    if (filterCount > 1) {
      removeFilterButton.style.display = "inline-block";
    }
  }
  if (filterCount >= 3) {
    addFilterButton.style.display = "none";
  }
});

removeFilterButton.addEventListener("click", function (event) {
  event.preventDefault();

  if (filterCount > 1) {
    const allFilterContainers =
      searchForm.querySelectorAll(".filter-container");
    if (allFilterContainers.length > 1) {
      const lastFilterToRemove =
        allFilterContainers[allFilterContainers.length - 1];
      searchForm.removeChild(lastFilterToRemove);
      filterCount--;
      if (filterCount <= 1) {
        removeFilterButton.style.display = "none";
      }
      addFilterButton.style.display = "inline-block";
    }
  }
  if (filterCount < 3) {
    addFilterButton.style.display = "inline-block";
  }
});

removeFilterButton.style.display = "none";
