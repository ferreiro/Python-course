% include('header.tpl')

	<h1 class="title">Results for your query:</h1>
	
	% if count <= 0:
		<h2 class="subtitle">
			No users found with that parameters values
		</h2> 
	% else:

		<h2 class="subtitle">
			<strong>{{count}}</strong> results
		</h2>

		<table style="width:100%">
			<tbody>

				<tr>
					<th><p>Country</p></th>
					<th><p>Number users</p></th>
				</tr>

				% for result in results:
					<tr>
						<td><p>{{ result['_id'] }}</p></td>
						<td><p>{{ result['value']['count'] }}</p></td>
					</tr>
				% end
			</tbody>
		</table>

	% end

% include('footer.tpl')