% include('header.tpl')

<h1>
	Delete all users by year
</h1>

<form action="/delete_year" method="POST">

	<fieldset class="input">
		<label for="year">
			Year to delete
		</label>
		<input name="year" type="text" placeholder="Year to delete" />
	</fieldset>

	<input type="submit" value="Send me!">
</form>

% include('footer.tpl')
