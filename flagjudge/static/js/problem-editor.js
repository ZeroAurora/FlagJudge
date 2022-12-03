var monaco; // should be imported in that page
let langSel = document.querySelector("#langsel");
let submitBtn = document.querySelector("#submit");

require.config({
  paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.34.1/min/vs" },
});

require(["vs/editor/editor.main"], function () {
  let monacoid = langSel.selectedOptions[0].dataset.monacoid;
  let editor = monaco.editor.create(document.getElementById("monaco"), {
    minimap: {
      enabled: false,
    },
    language: monacoid || langSel.value,
  });

  window.addEventListener("resize", function () {
    editor.layout();
  })

  langSel.addEventListener("change", function () {
    monacoid = langSel.selectedOptions[0].dataset.monacoid;
    monaco.editor.setModelLanguage(
      editor.getModel(),
      monacoid || langSel.value
    );
  });

  submitBtn.addEventListener("click", function () {
    const form = new FormData();
    form.append("language", langSel.value);
    form.append("code", editor.getValue());
    fetch("submit/", {
      method: "POST",
      body: form,
    })
      .then((resp) => resp.text())
      .then((queueid) => (window.location = `/queue/${queueid}/`));
  });
});
