<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand-md navbar-light bg-light sticky-top">
      <div class="container-fluid justify-content-between">
        <a class="text-dark" href="#">Curriculum</a>
        <a class="text-dark" href="#">API Projects/Scripts</a>
        <a class="text-dark" href="#">Database Projects</a>
        <a class="text-dark" href="#">Website projects</a>
        <a class="text-dark" href="#">Contact/Info</a>
        <div class="dropdown">
          <button
              class="btn btn-light dropdown-toggle"
              type="button"
              id="dropdownMenuButton1"
              data-bs-toggle="dropdown"
              aria-expanded="false"
          >
            Settings
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li>
              <a class="dropdown-item" href="/accounts/logout">Logout</a>
            </li>
          </ul>
        </div>
        <a class="text-dark" href="">Login</a>
      </div>
    </nav>
  </div>
</template>
