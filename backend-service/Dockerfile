FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY ["InnerVoice.Api.csproj", "./"]
RUN dotnet restore "InnerVoice.Api.csproj"

COPY . .
RUN dotnet publish "InnerVoice.Api.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app
COPY --from=build /app/publish .

EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000

ENTRYPOINT ["dotnet", "InnerVoice.Api.dll"]

