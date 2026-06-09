const ticketForm = document.getElementById('ticket-form');
const idInput = document.getElementById('ticket-id');
const titleInput = document.getElementById('title');
const descriptionInput = document.getElementById('description');
const priorityInput = document.getElementById('priority');
const statusInput = document.getElementById('status');
const technicianInput = document.getElementById('technician');
const saveButton = document.getElementById('save-btn');
const cancelButton = document.getElementById('cancel-btn');
const ticketList = document.getElementById('ticket-list');
const ticketCount = document.getElementById('ticket-count');
const formNote = document.getElementById('form-note');
const emptyState = document.getElementById('empty-state');
const statusFilters = document.getElementById('status-filters');
const priorityFilters = document.getElementById('priority-filters');
const clearFiltersButton = document.getElementById('clear-filters');
const themeToggleButton = document.getElementById('theme-toggle');

let tickets = [
  {
    id: 1,
    title: 'VPN access fails for remote user',
    description: 'User receives authentication timeout when connecting to the corporate VPN.',
    priority: 'High',
    status: 'Open',
    technician: 'A. Patel',
  },
  {
    id: 2,
    title: 'Email delivery delay in finance mailbox',
    description: 'Finance group mailbox has a 10-15 minute delay on inbound messages.',
    priority: 'Medium',
    status: 'In Progress',
    technician: 'J. Rivera',
  },
  {
    id: 3,
    title: 'Endpoint malware alert on laptop',
    description: 'Security tooling flagged suspicious process behavior requiring immediate triage.',
    priority: 'Critical',
    status: 'Open',
    technician: 'K. Morgan',
  },
  {
    id: 4,
    title: 'Printer queue stuck on 4th floor',
    description: 'Print jobs remain queued and never complete on shared network printer.',
    priority: 'Low',
    status: 'Resolved',
    technician: 'S. Lee',
  },
];

let isEditing = false;
let activeStatusFilter = 'All';
let activePriorityFilter = 'All';
let activeTheme = 'light';

function slugifyStatus(status) {
  return status.toLowerCase().replace(/\s+/g, '-');
}

function updateHeaderStats(visibleCount) {
  const totalCount = tickets.length;
  ticketCount.textContent = `${visibleCount} of ${totalCount} ticket${totalCount === 1 ? '' : 's'}`;
  emptyState.hidden = visibleCount !== 0;
}

function filterTickets(items) {
  return items.filter((ticket) => {
    const statusMatches = activeStatusFilter === 'All' || ticket.status === activeStatusFilter;
    const priorityMatches = activePriorityFilter === 'All' || ticket.priority === activePriorityFilter;
    return statusMatches && priorityMatches;
  });
}

function updateFilterButtons(container, selectedValue) {
  const buttons = container.querySelectorAll('.filter-btn');
  buttons.forEach((button) => {
    const isActive = button.dataset.filterValue === selectedValue;
    button.classList.toggle('is-active', isActive);
    button.setAttribute('aria-pressed', String(isActive));
  });
}

function clearFilters() {
  activeStatusFilter = 'All';
  activePriorityFilter = 'All';
  updateFilterButtons(statusFilters, activeStatusFilter);
  updateFilterButtons(priorityFilters, activePriorityFilter);
  renderTickets();
}

function applyTheme(theme) {
  activeTheme = theme === 'dark' ? 'dark' : 'light';
  document.body.setAttribute('data-theme', activeTheme);

  const isDark = activeTheme === 'dark';
  themeToggleButton.textContent = isDark ? 'Light Mode' : 'Dark Mode';
  themeToggleButton.setAttribute('aria-pressed', String(isDark));
  localStorage.setItem('ticketing-theme', activeTheme);
}

function toggleTheme() {
  applyTheme(activeTheme === 'dark' ? 'light' : 'dark');
}

function initializeTheme() {
  const savedTheme = localStorage.getItem('ticketing-theme');
  if (savedTheme === 'dark' || savedTheme === 'light') {
    applyTheme(savedTheme);
    return;
  }

  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(prefersDark ? 'dark' : 'light');
}

function resetForm() {
  ticketForm.reset();
  idInput.value = '';
  statusInput.value = 'Open';
  isEditing = false;
  saveButton.textContent = 'Create Ticket';
  cancelButton.hidden = true;
  formNote.textContent = '';
}

function fillFormForEdit(ticket) {
  idInput.value = String(ticket.id);
  titleInput.value = ticket.title;
  descriptionInput.value = ticket.description;
  priorityInput.value = ticket.priority;
  statusInput.value = ticket.status;
  technicianInput.value = ticket.technician;

  isEditing = true;
  saveButton.textContent = 'Save Changes';
  cancelButton.hidden = false;
  formNote.textContent = `Editing ticket #${ticket.id}`;
  titleInput.focus();
}

function createTicketElement(ticket) {
  const item = document.createElement('li');
  item.className = 'ticket';

  const statusClass = slugifyStatus(ticket.status);
  const priorityClass = ticket.priority.toLowerCase();

  item.innerHTML = `
    <article aria-labelledby="ticket-title-${ticket.id}">
      <div class="ticket-top">
        <h3 id="ticket-title-${ticket.id}">${ticket.title}</h3>
      </div>
      <div class="badges" aria-label="Ticket labels">
        <span class="badge priority-${priorityClass}">Priority: ${ticket.priority}</span>
        <span class="badge status-${statusClass}">Status: ${ticket.status}</span>
      </div>
      <p>${ticket.description}</p>
      <p class="meta">Assigned technician: <strong>${ticket.technician}</strong></p>
      <div class="ticket-actions" role="group" aria-label="Actions for ticket ${ticket.id}">
        <button type="button" data-action="edit" data-id="${ticket.id}">Edit</button>
        <button type="button" class="danger" data-action="close" data-id="${ticket.id}" ${ticket.status === 'Closed' ? 'disabled' : ''}>Close</button>
      </div>
    </article>
  `;

  return item;
}

function renderTickets() {
  const order = { Critical: 0, High: 1, Medium: 2, Low: 3 };
  const filtered = filterTickets(tickets);
  const sorted = [...filtered].sort((a, b) => {
    return order[a.priority] - order[b.priority] || a.id - b.id;
  });

  ticketList.innerHTML = '';
  sorted.forEach((ticket) => {
    ticketList.appendChild(createTicketElement(ticket));
  });

  updateHeaderStats(sorted.length);
}

function handleFilterSelection(event) {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement) || !target.classList.contains('filter-btn')) {
    return;
  }

  const filterType = target.dataset.filterType;
  const value = target.dataset.filterValue;
  if (!filterType || !value) {
    return;
  }

  if (filterType === 'status') {
    activeStatusFilter = value;
    updateFilterButtons(statusFilters, value);
  }

  if (filterType === 'priority') {
    activePriorityFilter = value;
    updateFilterButtons(priorityFilters, value);
  }

  renderTickets();
}

function validateForm() {
  if (!titleInput.value) {
    return 'Title is required.';
  }
  if (!descriptionInput.value) {
    return 'Description is required.';
  }
  if (!priorityInput.value) {
    return 'Priority is required.';
  }
  if (!statusInput.value) {
    return 'Status is required.';
  }
  if (!technicianInput.value) {
    return 'Assigned technician is required.';
  }
  return '';
}

function normalizeTextFields() {
  titleInput.value = titleInput.value.trim();
  descriptionInput.value = descriptionInput.value.trim();
  technicianInput.value = technicianInput.value.trim();
}

function handleSubmit(event) {
  event.preventDefault();

  normalizeTextFields();

  const error = validateForm();
  if (error) {
    formNote.textContent = error;
    return;
  }

  const payload = {
    title: titleInput.value,
    description: descriptionInput.value,
    priority: priorityInput.value,
    status: statusInput.value,
    technician: technicianInput.value,
  };

  if (isEditing) {
    const id = Number(idInput.value);
    tickets = tickets.map((ticket) => (ticket.id === id ? { ...ticket, ...payload } : ticket));
    formNote.textContent = `Ticket #${id} updated.`;
  } else {
    const id = tickets.length ? Math.max(...tickets.map((ticket) => ticket.id)) + 1 : 1;
    tickets.push({ id, ...payload });
    formNote.textContent = `Ticket #${id} created.`;
  }

  renderTickets();
  resetForm();
}

function handleTicketAction(event) {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) {
    return;
  }

  const action = target.dataset.action;
  const id = Number(target.dataset.id);
  if (!action || !id) {
    return;
  }

  const ticket = tickets.find((entry) => entry.id === id);
  if (!ticket) {
    return;
  }

  if (action === 'edit') {
    fillFormForEdit(ticket);
    return;
  }

  if (action === 'close') {
    tickets = tickets.map((entry) => {
      if (entry.id !== id) {
        return entry;
      }
      return { ...entry, status: 'Closed' };
    });

    if (isEditing && Number(idInput.value) === id) {
      statusInput.value = 'Closed';
    }

    formNote.textContent = `Ticket #${id} closed.`;
    renderTickets();
  }
}

ticketForm.addEventListener('submit', handleSubmit);
ticketList.addEventListener('click', handleTicketAction);
cancelButton.addEventListener('click', resetForm);
statusFilters.addEventListener('click', handleFilterSelection);
priorityFilters.addEventListener('click', handleFilterSelection);
clearFiltersButton.addEventListener('click', clearFilters);
themeToggleButton.addEventListener('click', toggleTheme);

renderTickets();
resetForm();
initializeTheme();
