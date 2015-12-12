    /* FUNCIONES PROPIAS */

function armar_hidden(prefix,valor,nombre,indice){
    var probando = "<input class="+'"'+"form-control"+'"'+
           " id="+'"'+prefix+"-"+indice+"-"+nombre+'"'
	   +" name="+'"'+prefix+"-"+indice+"-"+nombre+'"'
           +" type="+'"'+"hidden"+'"'
           + " value="+'"'+valor+'"'+">"
  return probando;
};

function armar_hidden_comun(valor,nombre){

    var probando = "<input class="+'"'+"form-control"+'"'+
           " id="+'"' +"id_"+nombre+'"'
	   +" name="+'"'+nombre+'"'
           +" type="+'"'+"hidden"+'"'
           + " value="+'"'+valor+'"'+">"
    return probando;
};


function armar_input(valor,nombre){
    var probando = "<input class="+'"'+"form-control"+'"'+
           " id="+'"'+nombre+'"'
	   +" name="+'"'+nombre+'"'
           +" type="+'"'+"hidden"+'"'
           + " value="+'"'+valor+'"'+">"
  return probando;
};

function imputs_llenos(inputs){
    var falso = 0;
    $(inputs).each(function(i,val){
        if (val.value == ""){
            falso = 1 ;
        }
    });
    if (falso == 1){
        alert("debe llenar todos los campos");
        return false;
    }

    return true;




}

function esFloatPositivo(num){
    
    var esFloat = /^[0-9]+(.[0-9]+)?/;
    if (esFloat.test(num) && (num>0)){
      return true}
    return false
    

}

function esEnteroPositivo(num){
  
    var isInt = /^[0-9]+/;
    if (isInt.test(num) && (num>0)){
      return true}
    return false
    
}


function eliminar_objeto(arreglo,indice){
        if (arreglo[indice].pk == undefined || arreglo[indice].pk ==""){ //
            arreglo.splice(indice,1);
          }else{
            arreglo[indice].delete_form="on";
        }
        return arreglo;
}

function cambio_cantidad(ele){
    ele.style.background="red";
    return true;
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

function esNatural(num){

    var isInt = /^[0-9]+/;
    if (isInt.test(num) && (num>=0)){
      return true}
    return false
    
}

function input_vacio(num){
  /* esta funcion recibe un INPUT. y verifica que su valor no sea vacio */

    if ($(num).val() == ""){
      return true;
    } 
    return false;
    
}








