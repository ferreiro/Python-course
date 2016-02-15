% include('header.tpl')

<h1>
	Delete user by username
</h1>

<form action="/delete" method="POST">

	<fieldset class="input">
		<label for="_id">
			Username
		</label>
		<input name="_id" type="text" value="" placeholder="Username" />
	</fieldset>

	<input type="submit" value="Send me!">
</form>

% include('footer.tpl')
