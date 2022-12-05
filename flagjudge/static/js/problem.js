var monaco; // should be imported in that page
const langSel = document.querySelector("#langsel");
const upload = document.querySelector("#upload");
const submitBtn = document.querySelector("#submit");

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
  });

  langSel.addEventListener("change", function () {
    monacoid = langSel.selectedOptions[0].dataset.monacoid;
    monaco.editor.setModelLanguage(
      editor.getModel(),
      monacoid || langSel.value
    );
  });

  upload.addEventListener("click", function () {
    let input = document.createElement("input");
    input.type = "file";
    input.addEventListener("change", function () {
      input.files[0].text().then(function (content) {
        editor.setValue(content);
      });
      input = null;
    });
    input.click();
  });

  submitBtn.addEventListener("click", function () {
    const form = new FormData();
    form.append("language", langSel.value);
    form.append("code", editor.getValue());
    fetch("submit/", {
      method: "POST",
      body: form,
    })
      .then((resp) => resp.json())
      .then((json) => {
        if (json) window.location = `/result/${json.submission}/`;
        else throw Error("Unable to judge");
      })
      .catch(() => {
        submitBtn.classList.remove("btn-primary");
        submitBtn.classList.add("btn-danger");
        submitBtn.innerHTML =
          "评测出现未知错误，请刷新页面，如反复出错请联系比赛管理员";
      });
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      正在评测，请稍等
    `;
  });
});
