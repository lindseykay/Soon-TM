import { gsap } from "gsap";

export default function reminderCreationAnimation(includeInput1) {
  const reminderCreation = gsap.timeline({ paused: true });

  if (includeInput1) {
    reminderCreation
      //phase 0 - show envelope
      .set(
        ".envelope-top",
        {
          top: 0,
          translateY: "-100%",
        },
        "phase-0"
      )
      .to(
        ".envelope",
        {
          duration: 0.5,
          display: "block",
          opacity: 1,
          bottom: "-40vh",
        },
        "phase-0"
      )
      //phase 1 - move contents down
      .set(
        ".submission-button",
        {
          display: "none",
        },
        "phase-0"
      )
      .to(
        ".form-input-4",
        {
          duration: 0.25,
          top: "20vh",
          opacity: 0,
        },
        "phase-1.1"
      )
      .to(
        ".form-input-3",
        {
          duration: 0.25,
          top: "30vh",
          opacity: 0,
        },
        "phase-1.2"
      )
      .to(
        ".form-input-2",
        {
          duration: 0.25,
          top: "40vh",
          opacity: 0,
        },
        "phase-1.3"
      )
      .to(
        ".form-input-1",
        {
          duration: 0.25,
          top: "50vh",
          opacity: 0,
        },
        "phase-1.4"
      )
      //close envelop lid
      .to(
        ".envelope-top",
        {
          duration: 0.5,
          zIndex: "2",
          scaleY: "-1",
          translateY: "+1",
        },
        "phase-2"
      )
      .to(
        ".envelope",
        {
          duration: 0.75,
          opacity: 0,
        },
        "phase-3"
      )
      .to(
        ".envelope",
        {
          duration: 1.5,
          bottom: "10vh",
        },
        "phase-3"
      )
      .set(
        ".form-input-1",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".form-input-2",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".form-input-3",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".form-input-4",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".submission-button",
        {
          display: "block",
          opacity: 0,
        },
        "phase-5"
      )
      .to(
        ".form-input-1",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".form-input-2",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".form-input-3",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".form-input-4",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".submission-button",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .set(
        ".envelope-top",
        {
          zIndex: "0",
          scaleY: "+1",
          translateY: "-1",
        },
        "phase-6"
      )
      .set(
        ".envelope",
        {
          bottom: "-50vh",
        },
        "phase-6"
      );
  } else {
    reminderCreation
      //phase 0 - show envelope
      .set(
        ".envelope-top",
        {
          top: 0,
          translateY: "-100%",
        },
        "phase-0"
      )
      .to(
        ".envelope",
        {
          duration: 0.5,
          display: "block",
          opacity: 1,
          bottom: "-40vh",
        },
        "phase-0"
      )
      //phase 1 - move contents down
      .set(
        ".submission-button",
        {
          display: "none",
        },
        "phase-0"
      )
      .to(
        ".form-input-4",
        {
          duration: 0.25,
          top: "20vh",
          opacity: 0,
        },
        "phase-1.1"
      )
      .to(
        ".form-input-3",
        {
          duration: 0.25,
          top: "30vh",
          opacity: 0,
        },
        "phase-1.2"
      )
      .to(
        ".form-input-2",
        {
          duration: 0.25,
          top: "40vh",
          opacity: 0,
        },
        "phase-1.3"
      )
      //close envelop lid
      .to(
        ".envelope-top",
        {
          duration: 0.5,
          zIndex: "2",
          scaleY: "-1",
          translateY: "+1",
        },
        "phase-2"
      )
      .to(
        ".envelope",
        {
          duration: 0.75,
          opacity: 0,
        },
        "phase-3"
      )
      .to(
        ".envelope",
        {
          duration: 1.5,
          bottom: "10vh",
        },
        "phase-3"
      )
      .set(
        ".form-input-2",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".form-input-3",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".form-input-4",
        {
          top: 0,
        },
        "phase-5"
      )
      .set(
        ".submission-button",
        {
          display: "block",
          opacity: 0,
        },
        "phase-5"
      )
      .to(
        ".form-input-2",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".form-input-3",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".form-input-4",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .to(
        ".submission-button",
        {
          duration: 1,
          opacity: 1,
        },
        "phase-6"
      )
      .set(
        ".envelope-top",
        {
          zIndex: "0",
          scaleY: "+1",
          translateY: "-1",
        },
        "phase-6"
      )
      .set(
        ".envelope",
        {
          bottom: "-50vh",
        },
        "phase-6"
      );
  }

  return reminderCreation;
}
