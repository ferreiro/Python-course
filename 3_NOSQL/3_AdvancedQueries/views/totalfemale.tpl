% include('header.tpl')
		
	<style type="text/css">
	body {
		background: red;
		background:url(fem.png);
		background-size: 60px auto;
	}
	.totalRounded {
		width: 400px;
		height: 400px;
		border-radius: 100%; 
		-webkit-border-radius: 100%; 
		-moz-border-radius: 100%; 
	  	margin: -200px 0 0 -200px;
		background: #f4f4f4;
	  	position: absolute;
	  	top: 50%;
	  	left: 50%;
	}
	.totalRounded_int {
		padding-top: 140px;
		text-align: center; 
	}
	footer {
		background:transparent;
		border: 0; 
	}
	footer p {
		color: #fff;
	}
	</style>

	<div class="totalRounded">
		<div class="totalRounded_int">
			<h2 class="subtitle">Females with 3 purchases</h2>
			<h1 class="title">Total: {{total}}</h1>
		</div>
	</div>

% include('footer.tpl')