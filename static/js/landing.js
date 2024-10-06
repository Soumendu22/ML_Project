const navId = document.getElementById("nav_menu"),
  ToggleBtnId = document.getElementById("toggle_btn"),
  CloseBtnId = document.getElementById("close_btn");

// ==== SHOW MENU ==== //
ToggleBtnId.addEventListener("click", () => {
  navId.classList.add("show");
});

// ==== HIDE MENU ==== //
CloseBtnId.addEventListener("click", () => {
  navId.classList.remove("show");
});

// ==== Animate on Scroll Initialize  ==== //
AOS.init();

// ==== GSAP Animations ==== //
// ==== LOGO  ==== //
gsap.from(".logo", {
  opacity: 0,
  y: -10,
  delay: 1,
  duration: 0.5,
});
// ==== NAV-MENU ==== //
gsap.from(".nav_menu_list .nav_menu_item", {
  opacity: 0,
  y: -10,
  delay: 1.4,
  duration: 0.5,
  stagger: 0.3,
});
// ==== TOGGLE BTN ==== //
gsap.from(".toggle_btn", {
  opacity: 0,
  y: -10,
  delay: 1.4,
  duration: 0.5,
});
// ==== MAIN HEADING  ==== //
gsap.from(".main-heading", {
  opacity: 0,
  y: 20,
  delay: 2.4,
  duration: 1,
});
// ==== INFO TEXT ==== //
gsap.from(".info-text", {
  opacity: 0,
  y: 20,
  delay: 2.8,
  duration: 1,
});
// ==== CTA BUTTONS ==== //
gsap.from(".btn_wrapper", {
  opacity: 0,
  y: 20,
  delay: 2.8,
  duration: 1,
});
// ==== TEAM IMAGE ==== //
gsap.from(".team_img_wrapper img", {
  opacity: 0,
  y: 20,
  delay: 3,
  duration: 1,
});

// Initialize AOS
AOS.init({
  duration: 1000, // Duration of animations in milliseconds
  easing: "ease-in-out", // Easing function for animations
});

document.addEventListener("DOMContentLoaded", function () {
  // Signup Dialog
  const openSignupDialogBtn = document.getElementById("openSignupDialog");
  const closeSignupDialogBtn = document.getElementById("closeSignupDialog");
  const signupDialog = document.getElementById("signupDialog");

  openSignupDialogBtn.addEventListener("click", function () {
    signupDialog.style.display = "flex";
  });

  closeSignupDialogBtn.addEventListener("click", function () {
    signupDialog.style.display = "none";
  });

  // Login Dialog
  const openLoginDialogBtn = document.getElementById("openLoginDialog");
  const closeLoginDialogBtn = document.getElementById("closeLoginDialog");
  const loginDialog = document.getElementById("loginDialog");

  openLoginDialogBtn.addEventListener("click", function () {
    loginDialog.style.display = "flex";
  });

  closeLoginDialogBtn.addEventListener("click", function () {
    loginDialog.style.display = "none";
  });

  // Close the dialog if user clicks outside of it
  window.addEventListener("click", function (event) {
    if (event.target === signupDialog) {
      signupDialog.style.display = "none";
    }
    if (event.target === loginDialog) {
      loginDialog.style.display = "none";
    }
  });
});

// $("#signupForm").on("submit", function (e) {
//   e.preventDefault();
//   $.ajax({
//     type: "POST",
//     url: "/signup",
//     data: $(this).serialize(),
//     success: function (response) {
//       // Assuming response includes `message` and `category`
//       if (response.success) {
//         displayMessage(response.message, "success"); // For success
//         // Optionally redirect after success
//         window.location.href = "/dashboard";
//       } else {
//         displayMessage(response.message, "danger"); // For failure
//       }
//     },
//     error: function (xhr, status, error) {
//       displayMessage("Something went wrong. Please try again.", "danger");
//     },
//   });
// });

// $("#loginForm").on("submit", function (e) {
//   e.preventDefault();
//   $.ajax({
//     type: "POST",
//     url: "/login",
//     data: $(this).serialize(),
//     success: function (response) {
//       // Assuming response includes `message` and `category`
//       if (response.success) {
//         displayMessage(response.message, "success"); // For success
//         // Optionally redirect after success
//         window.location.href = "/dashboard";
//       } else {
//         displayMessage(response.message, "danger"); // For failure
//       }
//     },
//     error: function (xhr, status, error) {
//       displayMessage("Login failed. Please try again.", "danger");
//     },
//   });
// });

// function displayMessage(message, category) {
//   const alertDiv = `<div class="alert alert-${category} alert-dismissible fade show" role="alert">
//                       ${message}
//                       <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
//                     </div>`;
//   $(".message-area").html(alertDiv); // Prepend the alert message to the `.message-area` div

//   setTimeout(function () {
//     $(".alert").alert("close");
//   }, 3000); // Close alert after 3 seconds
// }

// Signup Form Submission
// document
//   .querySelector("#signupForm")
//   .addEventListener("submit", async (event) => {
//     event.preventDefault();
//     const name = document.querySelector("#signupName").value;
//     const email = document.querySelector("#signupEmail").value;
//     const password = document.querySelector("#signupPassword").value;

//     try {
//       const response = await fetch("/signup", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ name, email, password }),
//       });

//       if (response.ok) {
//         alert("Signup successful!");
//         window.location.href = "/"; // Redirect after signup
//       } else {
//         alert("Signup failed");
//       }
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   });

// // Login Form Submission
// document
//   .querySelector("#loginForm")
//   .addEventListener("submit", async (event) => {
//     event.preventDefault();
//     const email = document.querySelector("#loginEmail").value;
//     const password = document.querySelector("#loginPassword").value;

//     try {
//       const response = await fetch("/login", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ email, password }),
//       });

//       if (response.ok) {
//         alert("Login successful!");
//         window.location.href = "/main"; // Redirect after login
//       } else {
//         alert("Login failed");
//       }
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   });
