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


function esFloatPositivo(num){
console.log("en esfloatpositiovo");
    var esFloat = /^[0-9]*(.[0-9]*)?$/;
    if (esFloat.test(num) && (num>=0)){
        return true}
    return false
}

function eliminar_objeto(arreglo,indice){
        console.log("pk ",arreglo[indice].pk );
        console.log("voy a borrar el insumo"+ arreglo[indice].texto);
        if (arreglo[indice].pk == undefined || arreglo[indice].pk ==""){ //
            arreglo.splice(indice,1);
            console.log("sefue");
          }else{
            arreglo[indice].delete_form="on";
            console.log("puse en on");
        }
        console.log("detalles despues ",arreglo);
        return arreglo;
}

function cambio_cantidad(i){
    document.getElementById("cantidad-"+i).style.background="red";

        }
function modificar_cantidad_arreglo(arreglo,nueva_cantidad,id_input,i){
    if (!esFloatPositivo(nueva_cantidad)){
        alert("debe ingresar una cantidad nueva valida");
    }else{
        arreglo[i].cantidad = nueva_cantidad;
        id_input.style.background="white";
    }
    return arreglo

}








