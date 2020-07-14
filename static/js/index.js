function myfunction(url)
{
    console.log(url)
    const request = new XMLHttpRequest();
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
	if (request.readyState === 4 && request.status === 200) {
	  console.log( request.responseText );

    }
    });
    request.send();
    console.log(url)
}


/* 
    <input type="button" value="function test" onclick="myfunction('/mark?source={{ i.image_name }}&state=true')"/>
    <input type="button" value="ok" onclick="window.location.href= '/mark?source={{ i.image_name }}&state=true'" />
    <input type="button" value="ne ok" onclick="window.location.href='/mark?source={{ i.image_name }}&state=false'" /> 

    <p> state {{ i.state }} they {{ i.xml_number }} ours {{ i.numbers_AI }}</p>
*/