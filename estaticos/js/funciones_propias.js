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

function armar_hidden_comun(valor,nombre){

    var probando = "<input class="+'"'+"form-control"+'"'+
           " id="+'"' +"id_"+nombre+'"'
	   +" name="+'"'+nombre+'"'
           +" type="+'"'+"hidden"+'"'
           + " value="+'"'+valor+'"'+">"
           console.log(probando);
    return probando;
};


function armar_input(valor,nombre){
    var probando = "<input class="+'"'+"form-control"+'"'+
           " id="+'"'+nombre+'"'
	   +" name="+'"'+nombre+'"'
           +" type="+'"'+"hidden"+'"'
           + " value="+'"'+valor+'"'+">"
           console.log(probando);
  return probando;
};



function esFloatPositivo(num){
    var esFloat = /^[0-9]+(.[0-9]+)?$/;
    if (esFloat.test(num) && (num>0)){
        return true}
    return false
}

function esEnteroPositivo(num){
    var isInt = /^[0-9]+$/;
    if (isInt.test(num) && (num>0)){
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
    if (!esEnteroPositivo(nueva_cantidad)){
        alert("la cantidad debe ser un entero positivo");
    }else{
        arreglo[i].cantidad = nueva_cantidad;
        id_input.style.background="white";
    }
    return arreglo

}








