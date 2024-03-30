$('#btn-novo-carro').on('click', () => {
  qtd_carros = $('input[name="qtd_carros"]').val();
  qtd_carros = parseInt(qtd_carros);
  qtd_carros += 1;

  let html_carros = ` \
    <div class="row carro" id="carro-${qtd_carros}"> \
      <div class="col-md-5 mb-3"> \
        <label for="modelo" class="form-label">Modelo</label> \
        <input type="text" name="modelo" id="modelo" class="form-control"> \
      </div> \
      <div class="col-md-3 mb-3"> \
        <label for="placa" class="form-label">Placa</label> \
        <input type="text" name="placa" id="placa" class="form-control"> \
      </div> \
      <div class="col-md-3 mb-3"> \
        <label for="ano" class="form-label">Ano</label> \
        <input type="text" name="ano" id="ano" class="form-control"> \
      </div> \
      <div class="col-md-1 mb-3"> \
        <label for="" class="form-label">Exluir</label> \
        <button type="button" class="btn btn-danger form-control" onclick="excluirCarro('carro-${qtd_carros}')"><i class="mdi mdi-delete"></i></button> \
      </div> \
    </div> \
  `;

  $('#form-carros').append(html_carros);
  $('input[name="qtd_carros"]').val(qtd_carros);
});

const excluirCarro = (cod_carro) => {
  obj = $(`#${cod_carro}`);
  id_carro = $(obj).find('#carro_id').val();
  if (id_carro) {
    console.log(id_carro);
    fetch(`http://localhost:8000/clientes/carros/${id_carro}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
      }
    }).then((result) => {
      result.json().then((data) => {
        $.NotificationApp.send('Notificação: ', data.message, 'top-right', data.result, 3e3, 1, 'slide');
      })
    });
  }
  obj.remove();
};

const pesquisarCliente = async (id_cliente) => {
  await fetch(`http://localhost:8000/clientes/${id_cliente}/`, {
    method: 'GET',
    headers: {
      'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
    }
  }).then((result) => {
    result.json().then((data) => {
      $('#id').val(id_cliente);
      for (x in data.cliente) {
        $(`#${x}`).val(data.cliente[x]);
      }

      $('#form-carros').html('');
      $('input[name="qtd_carros"]').val(0);
      data.carros.forEach(carro => {
        qtd_carros = $('input[name="qtd_carros"]').val();
        qtd_carros = parseInt(qtd_carros);
        qtd_carros += 1;

        let html_carros = ` \
          <div class="row carro" id="carro-${qtd_carros}"> \
            <input type="hidden" name="carro_id" id="carro_id" value="${carro.id}">
            <div class="col-md-5 mb-3"> \
              <label for="modelo" class="form-label">Modelo</label> \
              <input type="text" name="modelo" id="modelo" class="form-control" value="${carro.modelo}"> \
            </div> \
            <div class="col-md-3 mb-3"> \
              <label for="placa" class="form-label">Placa</label> \
              <input type="text" name="placa" id="placa" class="form-control" value="${carro.placa}"> \
            </div> \
            <div class="col-md-3 mb-3"> \
              <label for="ano" class="form-label">Ano</label> \
              <input type="text" name="ano" id="ano" class="form-control" value="${carro.ano}"> \
            </div> \
            <div class="col-md-1 mb-3"> \
              <label for="" class="form-label">Exluir</label> \
              <button type="button" class="btn btn-danger form-control" onclick="excluirCarro('carro-${qtd_carros}')"><i class="mdi mdi-delete"></i></button> \
            </div> \
          </div> \
        `;

        $('#form-carros').append(html_carros);
        $('input[name="qtd_carros"]').val(qtd_carros);
      });
    })
  });
};

$('.btn-salvar-cliente').on('click', async () => {
  const form_cliente = $('#form-cliente').serializeArray().reduce((output, value) => {
    output[value.name] = value.value
    return output
  }, {});

  form_cliente['carros'] = [];
  const list_carros = $('#form-carros .carro');
  list_carros.map((index, carro) => {
    form_cliente.carros.push({
      'carro_id': $(carro).find('input[name="carro_id"]').val(),
      'modelo': $(carro).find('input[name="modelo"]').val(),
      'placa': $(carro).find('input[name="placa"]').val(),
      'ano': $(carro).find('input[name="ano"]').val(),
    });
  });

  await fetch(`http://localhost:8000/clientes/${form_cliente.id}/`, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
    },
    body: JSON.stringify(form_cliente),
  }).then((result) => {
    result.json().then((data) => {
      if (data.result == 'success') {
        sessionStorage.setItem('PAGE_NOTIFICATION', JSON.stringify(data));
        window.location.reload();
      }

      $.NotificationApp.send('Notificação: ', data.message, 'top-right', data.result, 3e3, 1, 'slide');
    });
  })
});