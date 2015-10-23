    /* FUNCIONES PROPIAS */

function armar_hidden(prefix,valor,nombre,indice){
    console.log(nombre);
    console.log(valor);

    var probando = "<input class="+'"'+"form-control"+'"'+
           " id="+'"'+prefix+"-"+indice+"-"+nombre+'"'
	   +" name="+'"'+prefix+"-"+indice+"-"+nombre+'"'
           +" type="+'"'+"hidden"+'"'
           + " value="+'"'+valor+'"'+">"
           console.log(probando);
  return probando;
};


function armar_modif_tabla(objeto,nombre,atributo,indice){

	return "<tr>"
		+"<td>"+nombre+"</td>"
		+"<td><input id="+"nueva_cantidad-"+indice+" name="+"nueva_cantidad-"+indice+" value="+atributo+"></td>"
       + "<td><button type="+"button "+"data-id="+'"'+objeto+'"'
        +" id="+"renglon-"+objeto+" class="+"btn-eliminar"+" onClick= "+"eliminar("+objeto+") >Eliminar</button></td>"
       + "<td><button type="+"button "+"data-id="+'"'+objeto+'"'
        +" id="+"renglon-"+objeto+" class="+"btn-eliminar"+" onClick= "+"modificar("+objeto+","+indice+") >Modificar</button></td></tr>"
};








