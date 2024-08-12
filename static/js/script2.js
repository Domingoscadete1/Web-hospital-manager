const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

// Function to toggle active class on clicked menu item
function toggleActiveClass(clickedItem) {
  allSideMenu.forEach(item => {
    item.parentElement.classList.remove('active');
  });
  clickedItem.parentElement.classList.add('active');
}

allSideMenu.forEach(item => {
  item.addEventListener('click', function () {
    toggleActiveClass(this);
  });
});


//
// Função para armazenar o ID da página selecionada no localStorage
function storeSelectedPage(pageId) {
	localStorage.setItem('selectedPage', pageId);
  }
  
  // Função para recuperar o ID da página selecionada do localStorage
  function getSelectedPage() {
	return localStorage.getItem('selectedPage');
  }
  
  // Função para aplicar a classe 'active' ao item de menu correto
  function applyActiveClass(pageId) {
	allSideMenu.forEach(item => {
	  if (item.getAttribute('data-page-id') === pageId) {
		item.parentElement.classList.add('active');
	  } else {
		item.parentElement.classList.remove('active');
	  }
	});
  }
  
  // Ao carregar a página, verificar se há uma página selecionada armazenada
  const storedPageId = getSelectedPage();
  if (storedPageId) {
	applyActiveClass(storedPageId);
  }
  
  // Ao clicar em um item de menu, armazenar o ID da página e aplicar a classe 'active'
  allSideMenu.forEach(item => {
	item.addEventListener('click', function () {
	  const pageId = this.getAttribute('data-page-id');
	  storeSelectedPage(pageId);
	  toggleActiveClass(this);
	});
  });
// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
  sidebar.classList.toggle('hide');
});

// SEARCH FUNCTION (assuming you want to keep it)
const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
  if (window.innerWidth < 576) {
    e.preventDefault();
    searchForm.classList.toggle('show');
    if (searchForm.classList.contains('show')) {
      searchButtonIcon.classList.replace('bx-search', 'bx-x');
    } else {
      searchButtonIcon.classList.replace('bx-x', 'bx-search');
    }
  }
});

// PERSIST DARK MODE WITH LOCAL STORAGE

// Get the switch element
const switchMode = document.getElementById('switch-mode');

// Check if a dark mode preference exists in local storage
const isDarkMode = localStorage.getItem('darkMode') === 'true';

// Set the initial state based on local storage or default preference
if (isDarkMode) {
  document.body.classList.add('dark');
  switchMode.checked = true; // Reflect the stored preference in the switch
} else {
  document.body.classList.remove('dark');
  switchMode.checked = false;
}

// Toggle dark mode on switch change and update local storage
switchMode.addEventListener('change', function () {
  if (this.checked) {
    document.body.classList.add('dark');
    localStorage.setItem('darkMode', 'true'); // Store 'true' for dark mode
  } else {
    document.body.classList.remove('dark');
    localStorage.setItem('darkMode', 'false'); // Store 'false' for light mode
  }
});

// Responsive behavior on window resize (assuming you want to keep it)
if (window.innerWidth < 768) {
  sidebar.classList.add('hide');
} else if (window.innerWidth > 576) {
  searchButtonIcon.classList.replace('bx-x', 'bx-search');
  searchForm.classList.remove('show');
}

window.addEventListener('resize', function () {
  if (this.innerWidth > 576) {
    searchButtonIcon.classList.replace('bx-x', 'bx-search');
    searchForm.classList.remove('show');
  }
});

function isDarkModeEnabled() {
	return localStorage.getItem('darkMode') === 'true';
  }
  
  // Função para aplicar o modo escuro
  function applyDarkMode(enabled) {
	document.body.classList.toggle('dark', enabled);
	localStorage.setItem('darkMode', enabled);
  }
  
  // Verificar o modo escuro ao carregar a página
  if (isDarkModeEnabled()) {
	applyDarkMode(true);
  }
  
  // Evento para alternar o modo escuro
  switchMode.addEventListener('change', function () {
	applyDarkMode(this.checked);
  });