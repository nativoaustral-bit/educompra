/**
 * EduCompra Humm — Interacciones de interfaz de usuario
 * - Actualización dinámica de comunas según región (100% local, sin APIs externas)
 * - Manejo progresivo de adición a cotización (AJAX / feedback visual)
 */

document.addEventListener('DOMContentLoaded', function () {
  // --------------------------------------------------------------------------
  // 1. Selector de Regiones y Comunas Dinámico Local
  // --------------------------------------------------------------------------
  const regionSelect = document.getElementById('id_region');
  const comunaInput = document.getElementById('id_comuna');

  if (regionSelect && comunaInput && window.EDUCOMPRA_REGIONES) {
    // Si el campo de comuna es un input de texto, convertirlo o complementarlo con datalist
    let dataList = document.getElementById('comunas-datalist');
    if (!dataList) {
      dataList = document.createElement('datalist');
      dataList.id = 'comunas-datalist';
      document.body.appendChild(dataList);
      comunaInput.setAttribute('list', 'comunas-datalist');
    }

    function actualizarComunas() {
      const region = regionSelect.value;
      const comunas = window.EDUCOMPRA_REGIONES[region] || [];

      dataList.innerHTML = '';
      comunas.forEach(function (c) {
        const opt = document.createElement('option');
        opt.value = c;
        dataList.appendChild(opt);
      });

      // Si la comuna actual no pertenece a la nueva región, limpiarla
      if (comunaInput.value && !comunas.includes(comunaInput.value)) {
        comunaInput.value = '';
      }
    }

    regionSelect.addEventListener('change', actualizarComunas);
    if (regionSelect.value) {
      actualizarComunas();
    }
  }

  // --------------------------------------------------------------------------
  // 2. Adición a la Canasta con Mejora Progresiva (AJAX)
  // --------------------------------------------------------------------------
  const addCartForms = document.querySelectorAll('form.ajax-add-cart');
  addCartForms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      // Si el navegador soporta fetch, enviar asíncronamente
      if (!window.fetch) return;

      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerText : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Agregando...';
      }

      const formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Accept': 'application/json',
        },
        body: formData,
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.status === 'ok') {
            const badge = document.getElementById('header-canasta-count');
            if (badge) {
              badge.innerText = data.total_articulos;
            }
            if (submitBtn) {
              submitBtn.innerText = '✓ Agregado';
              setTimeout(function () {
                submitBtn.disabled = false;
                submitBtn.innerText = originalText;
              }, 1200);
            }
          } else {
            alert(data.mensaje || 'No se pudo agregar el producto.');
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.innerText = originalText;
            }
          }
        })
        .catch(function () {
          // Fallback a envío estándar si falla la red
          form.submit();
        });
    });
  });
});
